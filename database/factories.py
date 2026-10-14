"""
Factories: sahte (fake) ama ddd.md kısıtlarına uyan veri üretir.
Veritabanına yazmaz; yazma işi database/seed.py'dedir.
"""
from typing import Any, Dict, List, Optional

from faker import Faker

from database.tables import AnnouncementTable, UserTable

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
