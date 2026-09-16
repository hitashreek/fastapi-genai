from fastapi import FastAPI

app = FastAPI(
    title="Pincode lookup API",
    description="Auto fill city and state from Indian Pincode during checkout"
)

@app.get("/")
def root():
    return {"message":"Pincode lookup api"}