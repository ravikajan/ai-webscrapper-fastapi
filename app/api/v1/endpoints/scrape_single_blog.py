from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.llm_scraping import scrape_url

router = APIRouter()


DEFAULT_INSTRUCTION = """
Extract a Main Single ingore single blog post with its full content and necessary data from the given source. Return the result as a JSON object.

JSON Example

{
  "date": "X days ago",  // Could be "X days ago", "Y hours ago", "Z minutes ago", or an exact date
  "headline": "Title of the blog post",
  "content": "Full content of the blog post...",
  "media": [
    {
      "type": "image",
      "url": "https://example.com/image.jpg",
      "title": "Image Title"
    },
    {
      "type": "video",
      "url": "https://example.com/video.mp4",
      "title": "Video Title"
    }
  ],
  "tags": ["array of blog tags"]
}
"""

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="The URL to scrape")
    instruction: str = Field(
        default=DEFAULT_INSTRUCTION,
        description="Instruction for the LLM extraction strategy"
    )

@router.post("/scrape_single_blog")
async def scrape_single_blog(request: ScrapeRequest):
    instruction = request.instruction or DEFAULT_INSTRUCTION
    
    # Call the core scraping function
    result = scrape_url(request.url, instruction)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result