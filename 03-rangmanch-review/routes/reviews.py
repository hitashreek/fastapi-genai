from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session

# Create a router for review-related endpoints and grouped under "reviews".
router = APIRouter(prefix="/review", tags=["reviews"])

# Create a POST endpoint at /review/ and return the response using the ReviewRead schema.
@router.post("/", response_model=ReviewRead)
def create_review(
    
    # Request body is validated using the ReviewCreate model.
    review: ReviewCreate,

   # FastAPI automatically provides a database session using get_session.
    session: Session = Depends(get_session)
):
    # Convert the validated ReviewCreate data into a Review database object.
    db_review = Review(**review.model_dump())
    
    # Add the new review to the database session.
    session.add(db_review)
    
    # Save the changes to the database.
    session.commit()
    
    # Refresh the object to get database-generated values,
    # such as the new review ID and created_at.
    session.refresh(db_review)

    # Return the newly created review.
    return db_review