"""
Factories: sahte (fake) ama ddd.md kısıtlarına uyan veri üretir.
Veritabanına yazmaz; yazma işi database/seed.py'dedir.
"""
from typing import Any, Dict, List, Optional

from faker import Faker

from database.tables import AnnouncementTable, ApplicationTable, JobPostingTable, UserTable

DEPARTMENTS = [
    "Computer Engineering",
    "Software Engineering",
    "Electrical Engineering",
    "Industrial Engineering",
    "Business Administration",
    "Economics",
    "Law",
    "Medicine",
]


class BaseFactory:
    def __init__(self, seed: Optional[int] = None, locale: str = "tr_TR"):
        self.fake = Faker(locale)
        if seed is not None:
            Faker.seed(seed)


class UserFactory(BaseFactory):
    def build_data(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            # ck_users_email_lowercase ve uq_users_email kısıtları için
            "email": self.fake.unique.email().lower(),
            "graduation_year": self.fake.random_int(min=1990, max=2026),
            "department": self.fake.random_element(DEPARTMENTS),
        }
        data.update(overrides)
        return data

    def build(self, **overrides: Any) -> UserTable:
        return UserTable(**self.build_data(**overrides))

    def build_batch(self, count: int, **overrides: Any) -> List[UserTable]:
        return [self.build(**overrides) for _ in range(count)]


class AnnouncementFactory(BaseFactory):
    def build_data(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "title": self.fake.sentence(nb_words=5).rstrip("."),
            "content": self.fake.paragraph(nb_sentences=4),
            "author": self.fake.name(),
        }
        data.update(overrides)
        return data

    def build(self, **overrides: Any) -> AnnouncementTable:
        # created_at'i veritabanı (server_default now()) atar
        return AnnouncementTable(**self.build_data(**overrides))

    def build_batch(self, count: int, **overrides: Any) -> List[AnnouncementTable]:
        return [self.build(**overrides) for _ in range(count)]


JOB_TITLES = [
    "Backend Developer",
    "Frontend Developer",
    "Data Analyst",
    "DevOps Engineer",
    "Project Manager",
    "Financial Analyst",
    "Legal Counsel",
    "Research Assistant",
]
LOCATIONS = ["İstanbul", "Ankara", "İzmir", "Bursa", "Remote"]
# ck_job_postings_employment_type ile aynı değerler
EMPLOYMENT_TYPES = ["full_time", "part_time", "internship", "contract"]


class JobPostingFactory(BaseFactory):
    def build_data(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "title": self.fake.random_element(JOB_TITLES),
            "company": self.fake.company(),
            "location": self.fake.random_element(LOCATIONS),
            "employment_type": self.fake.random_element(EMPLOYMENT_TYPES),
            "description": self.fake.paragraph(nb_sentences=4),
            "is_active": self.fake.boolean(chance_of_getting_true=80),
            # posted_by seed.py tarafından (var olan kullanıcılardan) atanır
            "posted_by": None,
        }
        data.update(overrides)
        return data

    def build(self, **overrides: Any) -> JobPostingTable:
        # created_at'i veritabanı (server_default now()) atar
        return JobPostingTable(**self.build_data(**overrides))

    def build_batch(self, count: int, **overrides: Any) -> List[JobPostingTable]:
        return [self.build(**overrides) for _ in range(count)]


class ApplicationFactory(BaseFactory):
    STATUSES = ["pending", "reviewed", "accepted", "rejected"]

    def build_data(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            # job_posting_id / user_id seed.py tarafından atanır (FK)
            "job_posting_id": None,
            "user_id": None,
            "status": self.fake.random_element(self.STATUSES),
            "cover_letter": self.fake.paragraph(nb_sentences=3) if self.fake.boolean(chance_of_getting_true=70) else None,
        }
        data.update(overrides)
        return data

    def build(self, **overrides: Any) -> ApplicationTable:
        # applied_at'i veritabanı (server_default now()) atar
        return ApplicationTable(**self.build_data(**overrides))

    def build_batch(self, count: int, **overrides: Any) -> List[ApplicationTable]:
        return [self.build(**overrides) for _ in range(count)]
