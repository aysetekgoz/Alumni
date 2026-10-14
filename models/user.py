from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from sqlalchemy import func

from database.session import session_scope
from database.tables import UserTable


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    first_name: str
    last_name: str
    email: str
    graduation_year: int
    department: str


class UserUpdate(BaseModel):
    """Schema for full update of an existing user (PUT)."""
    first_name: str
    last_name: str
    email: str
    graduation_year: int
    department: str


class UserPatch(BaseModel):
    """Schema for partial update of an existing user (PATCH)."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    graduation_year: Optional[int] = None
    department: Optional[str] = None


def _row_to_dict(row: UserTable) -> Dict[str, Any]:
    return {
        "id": row.id,
        "first_name": row.first_name,
        "last_name": row.last_name,
        "email": row.email,
        "graduation_year": row.graduation_year,
        "department": row.department,
    }


def _normalize_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    """ddd.md: e-posta küçük harfle saklanır (ck_users_email_lowercase)."""
    if isinstance(payload.get("email"), str):
        payload["email"] = payload["email"].strip().lower()
    return payload


class User:
    """
    User Model backed by PostgreSQL (SQLAlchemy). Table: users (see ddd.md).
    The public CRUD API is unchanged: methods still return plain dictionaries,
    and return None when the id does not exist (controllers turn that into 404).
    Constraint violations (e.g. duplicate email) raise sqlalchemy IntegrityError,
    which main.py maps to HTTP 409.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        graduation_year: int,
        department: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.graduation_year = graduation_year
        self.department = department

    def to_dict(self) -> Dict[str, Any]:
        """Serializes user instance into a dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "graduation_year": self.graduation_year,
            "department": self.department,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Creates a User instance from a dictionary."""
        return cls(
            id=data.get("id"),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            graduation_year=data["graduation_year"],
            department=data["department"],
        )

    def save(self) -> "User":
        """
        Saves or updates the current instance in the database.
        """
        if self.id is None:
            created = User.create(self.to_dict())
            self.id = created["id"]
        else:
            User.update(self.id, self.to_dict())
        return self

    # ==========================================
    # CRUD Operations (Create, Read, Update, Delete)
    # ==========================================

    @classmethod
    def create(cls, data: Union[Dict[str, Any], UserCreate, "User"]) -> Dict[str, Any]:
        """
        [C - Create] Creates a new user record (the database assigns the ID).
        """
        if hasattr(data, "model_dump"):
            payload = data.model_dump()
        elif isinstance(data, cls):
            payload = data.to_dict()
        elif isinstance(data, dict):
            payload = dict(data)
        else:
            raise ValueError("Unsupported data format for User.create")

        payload = _normalize_email(payload)
        with session_scope() as session:
            row = UserTable(
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name"),
                email=payload.get("email"),
                graduation_year=payload.get("graduation_year"),
                department=payload.get("department"),
            )
            session.add(row)
            session.flush()  # id'yi almak için
            return _row_to_dict(row)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """
        [R - Read All] Retrieves all user records.
        """
        with session_scope() as session:
            rows = session.query(UserTable).order_by(UserTable.id).all()
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [R - Read by ID] Finds and returns a user record by its ID.
        Returns None if not found.
        """
        with session_scope() as session:
            row = session.get(UserTable, user_id)
            return _row_to_dict(row) if row else None

    @classmethod
    def get_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        """
        [R - Read by Email] Finds and returns a user record by email.
        Returns None if not found.
        """
        target_email = email.strip().lower()
        with session_scope() as session:
            row = session.query(UserTable).filter(UserTable.email == target_email).first()
            return _row_to_dict(row) if row else None

    @classmethod
    def update(cls, user_id: int, data: Union[Dict[str, Any], UserUpdate]) -> Optional[Dict[str, Any]]:
        """
        [U - Update (PUT)] Replaces all attributes of a user by ID.
        Returns the updated user record or None if not found.
        """
        if hasattr(data, "model_dump"):
            payload = data.model_dump()
        elif isinstance(data, dict):
            payload = dict(data)
        else:
            raise ValueError("Unsupported data format for User.update")

        payload = _normalize_email(payload)
        with session_scope() as session:
            row = session.get(UserTable, user_id)
            if row is None:
                return None
            for key in ("first_name", "last_name", "email", "graduation_year", "department"):
                setattr(row, key, payload.get(key, getattr(row, key)))
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def patch(cls, user_id: int, data: Union[Dict[str, Any], UserPatch]) -> Optional[Dict[str, Any]]:
        """
        [U - Patch (PATCH)] Partially updates fields of a user by ID.
        Returns the updated user record or None if not found.
        """
        if hasattr(data, "model_dump"):
            payload = data.model_dump(exclude_unset=True)
        elif isinstance(data, dict):
            payload = {k: v for k, v in data.items() if v is not None}
        else:
            raise ValueError("Unsupported data format for User.patch")

        payload = _normalize_email(payload)
        allowed = ("first_name", "last_name", "email", "graduation_year", "department")
        with session_scope() as session:
            row = session.get(UserTable, user_id)
            if row is None:
                return None
            for key, value in payload.items():
                if key in allowed:
                    setattr(row, key, value)
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def delete(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [D - Delete] Removes a user record by ID from storage.
        Returns the deleted record or None if not found.
        """
        with session_scope() as session:
            row = session.get(UserTable, user_id)
            if row is None:
                return None
            deleted = _row_to_dict(row)
            session.delete(row)
            return deleted

    @classmethod
    def count(cls) -> int:
        """Returns the total number of users."""
        with session_scope() as session:
            return session.query(func.count(UserTable.id)).scalar()

    @classmethod
    def clear(cls) -> None:
        """Clears all user records and resets the ID counter."""
        from sqlalchemy import text

        with session_scope() as session:
            session.execute(text("TRUNCATE TABLE users RESTART IDENTITY"))


if __name__ == "__main__":
    print("Testing User Model against the database (DATABASE_URL required)...")

    # 1. Test Create
    user1 = User.create({
        "first_name": "Ayşe",
        "last_name": "Tekgöz",
        "email": "ayse@example.com",
        "graduation_year": 2026,
        "department": "Computer Science"
    })
    print("Created User:", user1)

    # 2. Test Read All
    users = User.get_all()
    print("All Users:", users)

    # 3. Test Read By ID
    found_user = User.get_by_id(user1["id"])
    print("Found User:", found_user)

    # 4. Test Update (PUT)
    updated = User.update(user1["id"], {
        "first_name": "Ayşe Saliha",
        "last_name": "Tekgöz",
        "email": "ayse.tekgoz@example.com",
        "graduation_year": 2026,
        "department": "Computer Science"
    })
    print("Updated User:", updated)

    # 5. Test Patch (PATCH)
    patched = User.patch(user1["id"], {"department": "Software Engineering"})
    print("Patched User:", patched)

    # 6. Test Delete
    deleted = User.delete(user1["id"])
    print("Deleted User:", deleted)
    print("Remaining Users:", User.get_all())
