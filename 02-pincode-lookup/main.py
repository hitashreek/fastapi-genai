from fastapi import FastAPI
from exceptions import ( 
    PinCodeNotFoundError,       # custom errors
    pincode_not_found_handler,  # function
    InvalidPinCodeError,        # custom errors
    invalid_pincode_handler)    # function
from models import LocationResponse, BulkRequest, BulkResponse  # Pydantic models
from data import pincode_db     # import database

app = FastAPI(
    title="Pincode lookup API",
    description="Auto fill city and state from Indian Pincode during checkout"
)

# register your custom exception handler
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)

@app.get("/")
def root():
    return {"message":"Pincode lookup api"}


@app.get("/pincode/{code}", response_model=LocationResponse)    # {code} is a path parameter
def lookup_pincode(code: str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be exactly 6 digit")
    
    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    return pincode_db[code]
    
@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_looup(request: BulkRequest):
    results = []
    missing = []
    
    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else: 
            missing.append(code)
            
    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )
    