"""
Seeder: factory'lerle üretilen veriyi veritabanına yazar.

Kullanım (konteyner içinde):
    python -m database.seed                       # 20 mezun + 5 duyuru + 10 iş ilanı + 15 başvuru
    python -m database.seed --users 50 --announcements 10 --job-postings 30 --applications 40
    python -m database.seed --reset               # önce tabloları boşaltır
    python -m database.seed --seed 42             # tekrarlanabilir veri

Önce migration uygulanmış olmalı: alembic upgrade head
"""
import argparse

from sqlalchemy import text

from database.factories import AnnouncementFactory, ApplicationFactory, JobPostingFactory, UserFactory
from database.session import get_session_factory
from database.tables import AnnouncementTable, ApplicationTable, JobPostingTable, UserTable


def run_seed(users: int = 20, announcements: int = 5, job_postings: int = 10,
             applications: int = 15, reset: bool = False, seed: int | None = None) -> dict:
    Session = get_session_factory()
    with Session() as session:
        if reset:
            # id sayaçlarını da sıfırlar. job_postings/applications, users'a FK ile
            # bağlı olduğu için aynı TRUNCATE içinde listelenmek zorundadır.
            session.execute(text(
                "TRUNCATE TABLE users, announcements, job_postings, applications "
                "RESTART IDENTITY"
            ))

        user_rows = UserFactory(seed=seed).build_batch(users)
        announcement_rows = AnnouncementFactory(seed=seed).build_batch(announcements)

        session.add_all(user_rows)
        session.add_all(announcement_rows)
        session.flush()  # kullanıcı id'lerini al (posted_by FK için)

        # Her ilanın sahibi rastgele bir yeni mezun; ~%20'si sahipsiz (posted_by NULL)
        job_factory = JobPostingFactory(seed=seed)
        job_rows = []
        for _ in range(job_postings):
            poster = None
            if user_rows and job_factory.fake.boolean(chance_of_getting_true=80):
                poster = job_factory.fake.random_element(user_rows).id
            job_rows.append(job_factory.build(posted_by=poster))
        session.add_all(job_rows)
        session.flush()  # ilan id'lerini al (applications FK için)

        # Başvurular: (ilan, mezun) çiftleri benzersiz olmalı (uq_applications_job_user)
        app_factory = ApplicationFactory(seed=seed)
        pairs = {(j.id, u.id) for j in job_rows for u in user_rows}
        chosen = app_factory.fake.random_elements(list(pairs), length=min(applications, len(pairs)), unique=True) if pairs else []
        application_rows = [app_factory.build(job_posting_id=j, user_id=u) for j, u in chosen]
        session.add_all(application_rows)
        session.commit()

        return {
            "users_added": len(user_rows),
            "announcements_added": len(announcement_rows),
            "job_postings_added": len(job_rows),
            "applications_added": len(application_rows),
            "users_total": session.query(UserTable).count(),
            "announcements_total": session.query(AnnouncementTable).count(),
            "job_postings_total": session.query(JobPostingTable).count(),
            "applications_total": session.query(ApplicationTable).count(),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Veritabanını sahte veriyle doldur")
    parser.add_argument("--users", type=int, default=20)
    parser.add_argument("--announcements", type=int, default=5)
    parser.add_argument("--job-postings", type=int, default=10)
    parser.add_argument("--applications", type=int, default=15)
    parser.add_argument("--reset", action="store_true", help="Önce tabloları boşalt")
    parser.add_argument("--seed", type=int, default=None, help="Faker seed değeri")
    args = parser.parse_args()

    result = run_seed(args.users, args.announcements, args.job_postings,
                      args.applications, args.reset, args.seed)
    print(result)


if __name__ == "__main__":
    main()
