from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.llm_scraping import scrape_url  # Updated import

router = APIRouter()

DEFAULT_INSTRUCTION = """
Extract all blog posts from the given content that contain dates. Provide this information in a structured format, including the full content of each post. Due to the potential length of the content, use an artifact to present this information. The output should be in JSON format. Here's an example of the expected structure:
[
  {
    "date": "X days ago",
    "headline": "Title of the blog post",
    "content": "Full content of the blog post...",
    "image_url": "https://example.com/image.jpg",
    "slug_url": "/category/title-of-the-blog-post",
    "tags":["array of blog tags"]
  },
  {
    "date": "Y days ago",
    "headline": "Another blog post title",
    "content": "Full content of another blog post...",
    "image_url": "https://example.com/another-image.jpg",
    "slug_url": "/category/another-blog-post-title",
    "tags":["array of blog tags"]
  }
]
Ensure that all blog posts with dates are included, and that the full content is provided for each post.
"""

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="The URL to scrape")
    instruction: str = Field(
        default=DEFAULT_INSTRUCTION,
        description="Instruction for the LLM extraction strategy"
    )

@router.post("/scrape_url_data")
async def scrape_url_data(request: ScrapeRequest):
    # Use the provided instruction or the default if none is provided
    instruction = request.instruction or DEFAULT_INSTRUCTION
    
    # Call the core scraping function
    result = scrape_url(request.url, instruction)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result