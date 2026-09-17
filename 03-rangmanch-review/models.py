from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Review(SQLModel, table=True):  # Review represents DB table
    id: Optional[int] = Field(default=None, primary_key=True)  # ID is optional because the database generates it
    play_name: str = Field(index=True)  # Index makes searching by play_name faster
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    created_at: datetime = Field(default_factory=datetime.now)  # default_factory = generate the default value automatically 
    
    
class ReviewCreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    

class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int 
    comment: str
    created_at: datetime
    
    
class ReviewUpdate(SQLModel):  # Both fields are optional for partial updates.
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None