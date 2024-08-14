# import json
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field
# from crawl4ai import WebCrawler
# from app.config import settings

# router = APIRouter()

# def create_crawler():
#     crawler = WebCrawler()
#     crawler.warmup()
#     return crawler

# def run_crawler(url):
#     crawler = create_crawler()
#     result = crawler.run(url=url)
#     return result.extracted_content

# @router.get("/scrape_json")
# async def scrape_url_data():
#     try:
#         result = run_crawler("https://www.trtworld.com/europe/far-right-hooliganism-continues-for-fourth-day-across-uk-mosque-attacked-18191379")
#         return {
#             "success": True,
#             "raw_content": result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))