import os
import json
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy

load_dotenv()

class PlanetInformation(BaseModel):
    planet_name: str = Field(..., description="Name of the planet.")
    host_name: str = Field(..., description="Name of the planet host.")
    orbital_period: str = Field(..., description="Orbital period of the planet.")
    stellar_surface_gravity: str = Field(..., description="Stellar surface gravity of the planet.")


async def extract_structured_data_using_llm(
    provider: str, api_token: str = None, extra_headers: dict[str, str] = None
):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    browser_config = BrowserConfig(headless=False)

    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 2000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            provider=provider,
            api_token=api_token,
            schema=PlanetInformation.model_json_schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all mentioned plantes information. 
            Get information only on first 10 planets.""",
            extra_args=extra_args,
            verbose=True
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS", config=crawler_config
        )
        print(result.extracted_content)

if __name__ == "__main__":
    # Use ollama with llama3.3
    asyncio.run(
        extract_structured_data_using_llm(
            provider="openai/gpt-4o", api_token=os.getenv("OPENAI_API_KEY")
        )
    )

    # asyncio.run(
    #     extract_structured_data_using_llm(
    #         provider="openai/gpt-4o", api_token='ca963969ca3144f3a6e25501729bb680'
    #     )
    # )