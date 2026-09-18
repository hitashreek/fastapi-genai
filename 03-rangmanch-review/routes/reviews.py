from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session

router = APIRouter(prefix="/review", tags=["reviews"])  # Create a router for review-related endpoints and grouped under "reviews".
@router.post("/", response_model=ReviewRead)  # Create a POST endpoint at /review/ and return the response using the ReviewRead schema.
def create_review(
    review: ReviewCreate,  # Request body is validated using the ReviewCreate model. 
    session: Session = Depends(get_session)  # FastAPI automatically provides a database session using get_session.
):
    db_review = Review(**review.model_dump()) # Convert the validated ReviewCreate data into a Review database object.    
    session.add(db_review)  # Add the new review to the database session.        
    session.commit()  # Save the changes to the database.
    session.refresh(db_review) # Refresh the object to get database-generated values, such as the new review ID and created_at.
    return db_review # Return the newly created review.
    
    
@router.get("/", response_model=list[ReviewRead])  # Create a GET endpoint at /review/ that returns a list of reviews using the ReviewRead model.
def list_reviews(
    play_name: str | None = Query(None, description="Filter by Play name"),
    skip: int = Query(0, ge=0, description="No of review to skip/offset"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return"),
    session: Session = Depends(get_session)
):
    query = select(Review)  # creates a SQLModel query to select/retrieve records from the `Review` table.
    
    if play_name:
        query = query.where(Review.play_name == play_name)
        
    query = query.offset(skip).limit(limit)
    
    reviews = session.exec(query).all()
    return reviews
