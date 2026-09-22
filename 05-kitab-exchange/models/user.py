from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


# Database table for users
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str
    
    # one user can have many books
    books: list["Book"] = Relationship(back_populates="owner")
    

#request body for creating a user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str
    
# respose body 
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str
    

# avoid circular import  - Prevent two Python files from importing each other in a loop.
from models.book import Book
User.model_rebuild()
