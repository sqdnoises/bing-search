#!/usr/bin/python3

"""
# bing-search
Automate a browser to search random queries on Bing.
Copyright (C) 2024-present SqdNoises
License: MIT License
To view the full license, visit https://github.com/sqdnoises/bing-search#license
"""

import sys
import random
import asyncio
from pathlib import Path

import click
from tqdm import tqdm
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeout,
    Browser,
    BrowserContext,
    Page,
    Playwright
)

# Expanded list of common English words for generating random searches
WORDS = [
    # Common verbs
    "accept", "add", "admire", "admit", "advise", "afford", "agree", "alert", "allow", "amuse",
    "analyze", "announce", "annoy", "answer", "apologize", "appear", "applaud", "appreciate",
    "approve", "argue", "arrange", "arrest", "arrive", "ask", "attach", "attack", "attempt",
    "attend", "attract", "avoid", "back", "bake", "balance", "ban", "bang", "bare", "bat",
    
    # Common nouns
    "time", "person", "year", "way", "day", "thing", "man", "world", "life", "hand", 
    "part", "child", "eye", "woman", "place", "work", "week", "case", "point", "government",
    "company", "number", "group", "problem", "fact", "idea", "water", "money", "story", "fact",
    
    # Technology terms
    "computer", "software", "hardware", "internet", "website", "server", "database", "network",
    "security", "privacy", "cloud", "data", "algorithm", "application", "program", "code",
    "development", "testing", "debugging", "deployment", "framework", "library", "api",
    "interface", "system", "platform", "mobile", "desktop", "browser", "encryption",
    
    # Science terms
    "science", "physics", "chemistry", "biology", "mathematics", "experiment", "research",
    "theory", "hypothesis", "analysis", "laboratory", "scientist", "study", "discovery",
    "innovation", "technology", "engineering", "medicine", "quantum", "molecular",
    
    # Modern topics
    "artificial", "intelligence", "machine", "learning", "blockchain", "cryptocurrency",
    "virtual", "reality", "augmented", "robot", "automation", "sustainable", "renewable",
    "digital", "smart", "innovation", "startup", "social", "media", "streaming",
    
    # Everyday items
    "phone", "car", "house", "book", "food", "drink", "clothes", "shoes", "watch", "camera",
    "television", "radio", "newspaper", "magazine", "furniture", "kitchen", "bathroom",
    "bedroom", "garden", "office", "school", "restaurant", "store", "market", "bank",
    
    # Nature and environment
    "air", "water", "earth", "fire", "wind", "sun", "moon", "star", "planet", "ocean",
    "mountain", "river", "forest", "desert", "island", "climate", "weather", "animal",
    "plant", "tree", "flower", "bird", "fish", "insect", "ecosystem"
]

# Constants
COOKIES_PATH = Path.home() / ".bing-search" / "cookies.json"
BING_URL = "https://www.bing.com"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def get_random_search_query() -> str:
    """Generate a random search query using 2-7 random words."""
    return " ".join(random.choices(WORDS, k=random.randint(2, 7)))

def generate_search_queries(amount: int) -> list[str]:
    """Generate the specified amount of random search queries."""
    return [get_random_search_query() for _ in range(amount)]

async def setup_browser(playwright: Playwright) -> tuple[Browser, BrowserContext]:
    """Set up the browser with saved cookies if they exist."""
    try:
        # Launch browser with specific configuration for more natural behavior
        browser = await playwright.chromium.launch(
            headless = False,
            args = [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
            ]
        )
        
        context = await browser.new_context(
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            viewport = {"width": 1920, "height": 1080},
            java_script_enabled = True,
            bypass_csp = True,
            accept_downloads = True
        )
        
        # Modify the context to appear more human-like
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        if COOKIES_PATH.exists():
            try:
                cookies = COOKIES_PATH.read_text()
                await context.add_cookies(eval(cookies))
            except Exception as e:
                print(f"Warning: Failed to load cookies: {e}")
                print("You may need to sign in again.")
        
        return browser, context
    except Exception as e:
        print(f"Error setting up browser: {e}")
        raise

async def save_cookies(context: BrowserContext) -> None:
    """Save cookies from the current browser context."""
    try:
        cookies = await context.cookies()
        COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        COOKIES_PATH.write_text(str(cookies))
    except Exception as e:
        print(f"Error saving cookies: {e}")
        raise

async def perform_single_search(
    page: Page,
    query: str,
    progress_bar: tqdm
) -> bool:
    """Perform a single search with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            await page.goto(f"{BING_URL}/search?q={query}", timeout=30000)
            
            # Add random delays and scrolling for more human-like behavior
            await asyncio.sleep(random.uniform(1.0, 2.5))
            await page.mouse.move(
                random.randint(100, 700),
                random.randint(100, 700)
            )
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight * Math.random());")
            
            await page.wait_for_load_state("networkidle", timeout=10000)
            progress_bar.update(1)
            return True
        except PlaywrightTimeout:
            if attempt < MAX_RETRIES - 1:
                print(f'\nRetrying search for "{query}"...')
                await asyncio.sleep(RETRY_DELAY)
            else:
                print(f'\nFailed to complete search for "{query}" after {MAX_RETRIES} attempts')
                return False
        except Exception as e:
            print(f'\nUnexpected error during search for "{query}": {e}')
            return False

async def signin() -> None:
    """Handle the signin process and save cookies."""
    try:
        async with async_playwright() as playwright:
            browser, context = await setup_browser(playwright)
            page = await context.new_page()
            
            try:
                await page.goto(BING_URL)
                print("Please sign in to your Microsoft account.")
                print("Once signed in, press Enter to save cookies and exit.")
                input()
                
                await save_cookies(context)
                print("Cookies saved successfully!")
            except Exception as e:
                print(f"Error during signin process: {e}")
            finally:
                await browser.close()
    except Exception as e:
        print(f"Fatal error during signin: {e}")
        sys.exit(1)

async def perform_searches(search_amount: int) -> None:
    """Perform the specified number of random searches with progress tracking."""
    search_queries = generate_search_queries(search_amount)
    
    try:
        async with async_playwright() as playwright:
            browser, context = await setup_browser(playwright)
            
            if not COOKIES_PATH.exists():
                print('No saved cookies found. Please run "bing-search signin" first.')
                await browser.close()
                return
            
            with tqdm(total=search_amount, desc="Performing searches", unit="search") as progress_bar:
                pages: list[tuple[Page, str]] = []
                for query in search_queries:
                    try:
                        page = await context.new_page()
                        pages.append((page, query))
                    except Exception as e:
                        print(f"\nFailed to create new page: {e}")
                        continue
                
                for page, query in pages:
                    await page.bring_to_front()
                    await perform_single_search(page, query, progress_bar)
                    # Close the page after search is complete
                    await page.close()
                    # Randomized delay between searches
                    await asyncio.sleep(random.uniform(1.5, 3.0))
            
            print("Search session complete!")
            print("Attempted queries:")
            for _, query in pages:
                print(f"- {query}")
            
            await browser.close()
            print("Browser session closed.")
    
    except Exception as e:
        print(f"Fatal error during search session: {e}")
        sys.exit(1)

@click.group(name="bing-search")
def cli() -> None:
    """Automated Bing search tool with cookie persistence."""
    pass

@cli.command(name="signin")
def signin_command() -> None:
    """Sign in to Bing and save cookies."""
    asyncio.run(signin())

@cli.command(name="start")
@click.argument("random_searches_amount", type=int, default=5)
def start_command(random_searches_amount: int) -> None:
    """Start performing random searches on Bing."""
    if random_searches_amount <= 0:
        print("Error: Number of searches must be positive")
        return
    
    if random_searches_amount > 100:
        print("Warning: Large number of searches may be detected as automated activity")
        if not click.confirm("Do you want to continue?"):
            return
    
    asyncio.run(perform_searches(random_searches_amount))

if __name__ == "__main__":
    cli()