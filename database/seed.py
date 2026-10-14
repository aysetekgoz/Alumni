"""
Seeder: factory'lerle üretilen veriyi veritabanına yazar.

Kullanım (konteyner içinde):
    python -m database.seed                       # 20 mezun + 5 duyuru
    python -m database.seed --users 50 --announcements 10
    python -m database.seed --reset               # önce tabloları boşaltır
    python -m database.seed --seed 42             # tekrarlanabilir veri

Önce migration uygulanmış olmalı: alembic upgrade head
"""
import argparse

from sqlalchemy import text

from database.factories import AnnouncementFactory, UserFactory
from database.session import get_session_factory
from database.tables import AnnouncementTable, UserTable


def run_seed(users: int = 20, announcements: int = 5, reset: bool = False,
             seed: int | None = None) -> dict:
    Session = get_session_factory()
    with Session() as session:
        if reset:
            # id sayaçlarını da sıfırlar
            session.execute(text("TRUNCATE TABLE users, announcements RESTART IDENTITY"))

        user_rows = UserFactory(seed=seed).build_batch(users)
        announcement_rows = AnnouncementFactory(seed=seed).build_batch(announcements)

        session.add_all(user_rows)
        session.add_all(announcement_rows)
        session.commit()

        return {
            "users_added": len(user_rows),
            "announcements_added": len(announcement_rows),
            "users_total": session.query(UserTable).count(),
            "announcements_total": session.query(AnnouncementTable).count(),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Veritabanını sahte veriyle doldur")
    parser.add_argument("--users", type=int, default=20)
    parser.add_argument("--announcements", type=int, default=5)
    parser.add_argument("--reset", action="store_true", help="Önce tabloları boşalt")
    parser.add_argument("--seed", type=int, default=None, help="Faker seed değeri")
    args = parser.parse_args()

    result = run_seed(args.users, args.announcements, args.reset, args.seed)
    print(result)


if __name__ == "__main__":
    main()
