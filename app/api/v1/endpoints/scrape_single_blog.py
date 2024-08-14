from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.llm_scraping import scrape_url

router = APIRouter()


DEFAULT_INSTRUCTION = """
Extract the main single blog post with its full content and necessary data from the given source. The main blog post is the first one in the data array (index 0). Return the result as a JSON object.
Ignore any additional articles or blog posts in the array.
JSON Example:
{
"date": "X days ago",  // Could be "X days ago", "Y hours ago", "Z minutes ago", or an exact date
"headline": "Title of the main blog post",
"content": "Full content of the main blog post...",
"media": [
{
"type": "image",
"url": "https://example.com/image.jpg",
"title": "Image Title"
}
],
"tags": ["array of blog tags"]
}
Note: Only include media and tags that are directly associated with the main blog post (index 0 in the data array). Do not include information from other articles or related content.
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