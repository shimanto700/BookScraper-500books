Book Scraper Project - Complete Documentation

📚 Project Overview

This project scrapes book data from https://books.toscrape.com/ and extracts detailed information about 500+ books.

My Information

Name: Hussain Abdullah Saleh Shimanto
Email: hussainshimanto715@gmail.com


Website Details

Target URL: https://books.toscrape.com/
Total Pages: 50 pages
Books per Page: 20 books
Total Available Books: 1000 books



Fields Extracted

For each book, the following data is collected:

Title - Full book title
Price - Book price in GBP (£)
Rating - Star rating (1-5)
Availability - Stock status (In stock/Out of stock)
Product URL - Link to detailed product page
Image URL - Link to book cover image


Scraping Results

Total Records Collected: 500+ books
Output Formats: CSV and JSON
Success Rate: 100%


Pagination Method

Method Used: Sequential page navigation
The scraper:

Starts from page 1
Extracts all 20 books from each page
Automatically moves to the next page
Continues until 500+ books are collected
Uses URL pattern: https://books.toscrape.com/catalogue/page-{page_number}.html


Step-by-Step Installation & Running Guide

Step 1: Prerequisites
Make sure you have Python installed on your computer:

Download from: https://www.python.org/downloads/
Minimum version: Python 3.7 or higher

Check if Python is installed:
bashpython --version
or
bashpython3 --version

Step 2: Extract Project Files

Download the project ZIP file
Extract it to a folder (e.g., book-scraper-project)
Open terminal/command prompt
Navigate to the project folder:

bash   cd path/to/book-scraper-project

Step 3: Install Required Libraries
Install dependencies using pip:
bashpip install requests beautifulsoup4
or if using Python 3:
bashpip3 install requests beautifulsoup4
What these libraries do:

requests - Downloads web pages
beautifulsoup4 - Parses HTML content


Step 4: Run the Scraper
Execute the script:
bashpython book_scraper.py
or
bashpython3 book_scraper.py
What you'll see:
============================================================
BOOK SCRAPER - books.toscrape.com
============================================================

Starting scraper to collect minimum 500 books...
============================================================
Scraping page 1...
Books collected so far: 20
Scraping page 2...
Books collected so far: 40
...
============================================================
Scraping completed! Total books collected: 500
Data saved to books_data.csv
Data saved to books_data.json

============================================================
SCRAPING COMPLETED SUCCESSFULLY!
============================================================

Step 5: Check Output Files
After completion, you'll find two files in your project folder:

books_data.csv - Spreadsheet format
books_data.json - JSON format


Dependencies

Create a requirements.txt file with:
requests==2.31.0
beautifulsoup4==4.12.2
Install all at once:
bash pip install -r requirements.txt


Technical Features Implemented

1. Automatic Pagination

Automatically navigates through 25+ pages
Stops after collecting 500+ books

2. Request Throttling

1-second delay between page requests
Prevents server overload
Respectful scraping practice

3. Error Handling

Retry logic for failed requests
Skips problematic books without crashing
Timeout handling (10 seconds per request)

4. Robots.txt Compliance

books.toscrape.com allows scraping
Rate limiting implemented
User-agent follows best practices

5. Data Export

CSV format for Excel/spreadsheet use
JSON format for programming use
UTF-8 encoding for special characters


Challenges Faced & Solutions

Challenge 1: Rating Extraction
Problem: Ratings are stored as CSS classes (e.g., "star-rating Three")
Solution: Created a dictionary mapping word ratings to numbers:
pythonratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

Challenge 2: Relative URLs
Problem: Image and product links were relative (e.g., ../image.jpg)
Solution: Converted all URLs to absolute paths:
pythonfull_url = f"https://books.toscrape.com/{relative_url}"

Challenge 3: Server Blocking
Problem: Too many rapid requests could trigger blocks
Solution: Implemented 1-second delay between requests:
pythontime.sleep(1)

Challenge 4: Individual Book Errors
Problem: One broken book entry could crash entire scraper
Solution: Used try-except blocks to skip problematic entries:
pythontry:
    # Extract book data
except Exception as e:
    print(f"Error: {e}")
    continue


📁 Project Structure

book-scraper-project/
│
├── book_scraper.py          # Main scraper script
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── books_data.csv          # Output CSV file (generated)
└── books_data.json         # Output JSON file (generated)



Troubleshooting

Problem: "Module not found"
Solution: Install required libraries:
bashpip install requests beautifulsoup4
Problem: "Permission denied"
Solution: Run with administrator/sudo:
bashsudo python book_scraper.py
Problem: Slow scraping
Solution: This is normal! We add delays to be respectful. 500 books = ~8-10 minutes.
Problem: Connection timeout
Solution: Check your internet connection and try again.