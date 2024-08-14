import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from crawl4ai.web_crawler import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from app.config import settings

router = APIRouter()

DEFAULT_INSTRUCTION = """
Extract the following information from a given web page:
1. Title: The main title of the article or page
2. Description: A brief summary or description of the content
3. Date: The publication date of the article
4. Image: URL of the main image associated with the content

Format the extracted data as a JSON object with the following structure:

{
  "title": "Extracted title",
  "description": "Extracted description",
  "date": "Extracted date",
  "image": "URL of the extracted image",
  "error": false
}

If unable to extract the data, set "error" to true.
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
            "error": f"Scraping failed: {str(e)}"
        }