import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from crawl4ai.web_crawler import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from app.config import settings

router = APIRouter()

DEFAULT_INSTRUCTION = """
Extract all blog posts from the given content that contain dates. Provide this information in a structured format, including the full content of each post. Due to the potential length of the content, use an artifact to present this information. The output should be in JSON format. Here's an example of the expected structure:
jsonCopy[
  {
    "date": "X days ago",
    "headline": "Title of the blog post",
    "content": "Full content of the blog post...",
    "image_url": "https://example.com/image.jpg",
    "slug_url": "/category/title-of-the-blog-post"
  },
  {
    "date": "Y days ago",
    "headline": "Another blog post title",
    "content": "Full content of another blog post...",
    "image_url": "https://example.com/another-image.jpg",
    "slug_url": "/category/another-blog-post-title"
  }
]
Ensure that all blog posts with dates are included, and that the full content is provided for each post.
Is this more in line with what you were looking for? The prompt now includes a clear JSON example to illustrate the expected format of the output.
"""

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="The URL to scrape")
    instruction: str = Field(
        default=DEFAULT_INSTRUCTION,
        description="Instruction for the LLM extraction strategy"
    )

@router.post("/scrape_url_data")
async def scrape_url_data(request: ScrapeRequest):
    try:
        crawler = WebCrawler()
        crawler.warmup()
        
        # Use the provided instruction or the default if none is provided
        instruction = request.instruction or DEFAULT_INSTRUCTION
        
        result = crawler.run(
            url=request.url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4",
                api_token=settings.OPENAI_API_KEY,
                extraction_type="schema",
                instruction=instruction
            ),
            bypass_cache=True,
        )
        
        if result.extracted_content is None:
            return {
                "success": False,
                "error": "No content was extracted",
                "raw_content": None
            }
        
        try:
            extracted_data = json.loads(result.extracted_content)
        except json.JSONDecodeError as json_error:
            return {
                "success": False,
                "error": f"Failed to parse JSON: {str(json_error)}",
                "raw_content": result.extracted_content
            }
        
        # Optionally save to file
        # with open(".data/data.json", "w", encoding="utf-8") as f:
        #     f.write(result.extracted_content)
        
        return {
            "success": True,
            "data": extracted_data,
            "count": len(extracted_data) if isinstance(extracted_data, list) else 1
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Scraping failed: {str(e)}",
            "raw_content": getattr(result, 'extracted_content', None) if 'result' in locals() else None
        }