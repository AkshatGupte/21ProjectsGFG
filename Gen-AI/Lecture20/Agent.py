import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, ChatGoogle  

async def main():
    llm = ChatGoogle(model="gemini-2.0-flash") 

    task = """
    Go to Google. Search: One piece anime characters with logia devil fruits.
    From the search results page, extract ONLY the first 3 organic results.
    For each result, capture:
      - Title
      - URL
    Return them as a JSON list like:
    [
      {"title": "...", "url": "..."},
      {"title": "...", "url": "..."},
      {"title": "...", "url": "..."}
    ]
    """

    agent = Agent(task=task, llm=llm)
    result = await agent.run()

    try:
        result = agent.history.final_result()
        if not result:
            result = agent.history.extracted_content()
        print("\nTop 3 results:")
        print(result)
    except Exception as e:
        print("No extracted content:", e)


    try:
        urls = agent.history.urls()
    except Exception:
        urls = []
    print("\nVisited URLs:", urls)

    # Save visited URLs
    with open("Visited_urls.txt", "w", encoding="utf-8") as f:
        for url in urls:
            f.write(str(url) + "\n")
    print("\nVisited_urls.txt created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
