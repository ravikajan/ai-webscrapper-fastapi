from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "Welcome to the FastAPI Scraper"}