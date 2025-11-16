import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
from urllib.parse import urljoin
from typing import List, Dict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BookScraper:
    """
    Web scraper for books.toscrape.com
    Extracts book data with pagination handling and exports to CSV/JSON
    """
    
    def __init__(self, base_url: str = "https://books.toscrape.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.books_data: List[Dict] = []
        self.max_retries = 3
        self.delay_range = (1, 3)  # Random delay between 1-3 seconds
        
    def get_page(self, url: str, retry_count: int = 0) -> BeautifulSoup:
        """
        Fetch page with error handling and retry logic
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Add delay to be respectful
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            if retry_count < self.max_retries:
                logger.warning(f"Request failed, retrying... ({retry_count + 1}/{self.max_retries})")
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self.get_page(url, retry_count + 1)
            else:
                logger.error(f"Failed to fetch {url} after {self.max_retries} retries: {e}")
                raise
    
    def extract_rating(self, article) -> str:
        """
        Extract star rating from book article
        """
        rating_map = {
            'One': '1',
            'Two': '2',
            'Three': '3',
            'Four': '4',
            'Five': '5'
        }
        
        rating_elem = article.find('p', class_='star-rating')
        if rating_elem:
            for rating_text, rating_num in rating_map.items():
                if rating_text in rating_elem.get('class', []):
                    return rating_num
        return 'N/A'
    
    def extract_book_data(self, article, page_url: str) -> Dict:
        """
        Extract all required data from a book article element
        """
        book_data = {}
        
        # Title
        title_elem = article.find('h3').find('a')
        book_data['title'] = title_elem.get('title', 'N/A')
        
        # Product detail page link
        relative_link = title_elem.get('href', '')
        book_data['product_url'] = urljoin(page_url, relative_link)
        
        # Price
        price_elem = article.find('p', class_='price_color')
        book_data['price'] = price_elem.text.strip() if price_elem else 'N/A'
        
        # Rating
        book_data['rating'] = self.extract_rating(article)
        
        # Stock availability
        stock_elem = article.find('p', class_='instock availability')
        if stock_elem:
            stock_text = stock_elem.text.strip()
            book_data['availability'] = 'In stock' if 'in stock' in stock_text.lower() else 'Out of stock'
        else:
            book_data['availability'] = 'Unknown'
        
        # Image URL
        img_elem = article.find('img')
        if img_elem:
            relative_img = img_elem.get('src', '')
            book_data['image_url'] = urljoin(self.base_url, relative_img)
        else:
            book_data['image_url'] = 'N/A'
        
        return book_data
    
    def scrape_page(self, page_url: str) -> int:
        """
        Scrape all books from a single page
        Returns the number of books scraped
        """
        try:
            soup = self.get_page(page_url)
            
            # Find all book articles
            articles = soup.find_all('article', class_='product_pod')
            
            for article in articles:
                try:
                    book_data = self.extract_book_data(article, page_url)
                    self.books_data.append(book_data)
                except Exception as e:
                    logger.error(f"Error extracting book data: {e}")
                    continue
            
            logger.info(f"Scraped {len(articles)} books from page")
            return len(articles)
            
        except Exception as e:
            logger.error(f"Error scraping page {page_url}: {e}")
            return 0
    
    def get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> str:
        """
        Find the next page URL from pagination
        """
        next_button = soup.find('li', class_='next')
        if next_button:
            next_link = next_button.find('a')
            if next_link:
                relative_url = next_link.get('href', '')
                return urljoin(current_url, relative_url)
        return None
    
    def scrape_books(self, min_books: int = 500) -> List[Dict]:
        """
        Main scraping function with pagination
        Scrapes until minimum number of books is reached
        """
        logger.info(f"Starting scrape - Target: {min_books} books")
        
        current_url = self.base_url
        page_count = 0
        
        while len(self.books_data) < min_books:
            page_count += 1
            logger.info(f"Scraping page {page_count} - Total books: {len(self.books_data)}")
            
            # Scrape current page
            books_scraped = self.scrape_page(current_url)
            
            if books_scraped == 0:
                logger.warning("No books found on page, stopping")
                break
            
            # Check if we've reached the target
            if len(self.books_data) >= min_books:
                logger.info(f"Target reached! Scraped {len(self.books_data)} books")
                break
            
            # Get next page URL
            try:
                soup = self.get_page(current_url)
                next_url = self.get_next_page_url(soup, current_url)
                
                if not next_url:
                    logger.info("No more pages to scrape")
                    break
                
                current_url = next_url
                
            except Exception as e:
                logger.error(f"Error finding next page: {e}")
                break
        
        logger.info(f"Scraping complete! Total books: {len(self.books_data)}")
        return self.books_data
    
    def export_to_csv(self, filename: str = "books_data.csv"):
        """
        Export scraped data to CSV file
        """
        if not self.books_data:
            logger.warning("No data to export")
            return
        
        fieldnames = ['title', 'price', 'rating', 'availability', 'product_url', 'image_url']
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.books_data)
            
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
    
    def export_to_json(self, filename: str = "books_data.json"):
        """
        Export scraped data to JSON file
        """
        if not self.books_data:
            logger.warning("No data to export")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(self.books_data, jsonfile, indent=2, ensure_ascii=False)
            
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")


def main():
    """
    Main execution function
    """
    # Initialize scraper
    scraper = BookScraper()
    
    # Check robots.txt compliance
    print("=" * 60)
    print("Book Scraper - books.toscrape.com")
    print("=" * 60)
    print("\nNote: This website allows scraping (check robots.txt)")
    print("Implementing responsible scraping with delays...\n")
    
    # Scrape books
    try:
        books = scraper.scrape_books(min_books=500)
        
        print(f"\n{'=' * 60}")
        print(f"Successfully scraped {len(books)} books!")
        print(f"{'=' * 60}\n")
        
        # Export data
        scraper.export_to_csv("books_data.csv")
        scraper.export_to_json("books_data.json")
        
        # Display sample data
        print("\nSample of scraped data (first 3 books):")
        print("-" * 60)
        for i, book in enumerate(books[:3], 1):
            print(f"\nBook {i}:")
            print(f"  Title: {book['title']}")
            print(f"  Price: {book['price']}")
            print(f"  Rating: {book['rating']} stars")
            print(f"  Availability: {book['availability']}")
            print(f"  URL: {book['product_url']}")
        
        print(f"\n{'=' * 60}")
        print("Data exported to:")
        print("  - books_data.csv")
        print("  - books_data.json")
        print(f"{'=' * 60}\n")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()