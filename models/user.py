from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel


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


class User:
    """
    User Model without database connection.
    Encapsulates user data and in-memory CRUD operations.
    """

    # In-memory storage acting as a simulated database table
    _db: List[Dict[str, Any]] = []
    _auto_increment_id: int = 1

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
        Saves or updates the current instance in the in-memory database.
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
        [C - Create] Creates a new user record with an auto-incrementing ID.
        """
        if hasattr(data, "model_dump"):
            payload = data.model_dump()
        elif isinstance(data, cls):
            payload = data.to_dict()
        elif isinstance(data, dict):
            payload = dict(data)
        else:
            raise ValueError("Unsupported data format for User.create")

        user_id = cls._auto_increment_id
        cls._auto_increment_id += 1

        new_user = {
            "id": user_id,
            "first_name": payload.get("first_name"),
            "last_name": payload.get("last_name"),
            "email": payload.get("email"),
            "graduation_year": payload.get("graduation_year"),
            "department": payload.get("department"),
        }
        cls._db.append(new_user)
        return new_user

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """
        [R - Read All] Retrieves all user records.
        """
        return cls._db

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [R - Read by ID] Finds and returns a user record by its ID.
        Returns None if not found.
        """
        for user in cls._db:
            if user["id"] == user_id:
                return user
        return None

    @classmethod
    def get_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        """
        [R - Read by Email] Finds and returns a user record by email.
        Returns None if not found.
        """
        target_email = email.strip().lower()
        for user in cls._db:
            if user.get("email", "").strip().lower() == target_email:
                return user
        return None

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

        for user in cls._db:
            if user["id"] == user_id:
                user["first_name"] = payload.get("first_name", user["first_name"])
                user["last_name"] = payload.get("last_name", user["last_name"])
                user["email"] = payload.get("email", user["email"])
                user["graduation_year"] = payload.get("graduation_year", user["graduation_year"])
                user["department"] = payload.get("department", user["department"])
                return user
        return None

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

        for user in cls._db:
            if user["id"] == user_id:
                user.update(payload)
                return user
        return None

    @classmethod
    def delete(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [D - Delete] Removes a user record by ID from storage.
        Returns the deleted record or None if not found.
        """
        for index, user in enumerate(cls._db):
            if user["id"] == user_id:
                return cls._db.pop(index)
        return None

    @classmethod
    def count(cls) -> int:
        """Returns the total number of users."""
        return len(cls._db)

    @classmethod
    def clear(cls) -> None:
        """Clears all user records and resets the ID counter."""
        cls._db.clear()
        cls._auto_increment_id = 1


if __name__ == "__main__":
    print("Testing User Model without database connection...")
    
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
    found_user = User.get_by_id(1)
    print("Found User (ID 1):", found_user)

    # 4. Test Update (PUT)
    updated = User.update(1, {
        "first_name": "Ayşe Saliha",
        "last_name": "Tekgöz",
        "email": "ayse.tekgöz@example.com",
        "graduation_year": 2026,
        "department": "Computer Science"
    })
    print("Updated User:", updated)

    # 5. Test Patch (PATCH)
    patched = User.patch(1, {"department": "Software Engineering"})
    print("Patched User:", patched)

    # 6. Test Delete
    deleted = User.delete(1)
    print("Deleted User:", deleted)
    print("Remaining Users:", User.get_all())
