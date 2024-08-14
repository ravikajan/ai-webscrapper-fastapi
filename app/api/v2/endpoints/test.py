from fastapi import APIRouter

router = APIRouter()

@router.get("/testv2")
async def test():
    return {"message": "Welcome to the FastAPI Scraper"}