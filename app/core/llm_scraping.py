import json
from crawl4ai.web_crawler import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from app.config import settings

def scrape_url(url: str, instruction: str) -> dict:
    try:
        crawler = WebCrawler()
        crawler.warmup()
        
        result = crawler.run(
            url=url,
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