# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import time

# def scrape_real_estate_news(url="https://realestate.usnews.com/topics/subjects/real-estate", limit=15):
#     options = Options()
#     options.headless = True
    
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)
    
#     time.sleep(5)
    
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()
    
#     print("HTML preview:")
#     print(soup.prettify()[:500])
    
#     articles = []
#     containers = soup.find_all("div", class_="Box-w0dun1-0 MediaObject__Content-sc-19vl09d-3 bcZeaE lhdCWz")
    
#     for idx, container in enumerate(containers):
#         if idx >= limit:
#             break
        
#         h3 = container.find("h3", class_="Heading-sc-1w5xk2o-0 kGRSaK story-headline")
#         if h3:
#             a_tag = h3.find("a")
#             if a_tag:
#                 headline_text = a_tag.get_text(strip=True)
#                 article_url = a_tag.get("href", "")
#                 if article_url and article_url.startswith("/"):
#                     article_url = "https://realestate.usnews.com" + article_url
#             else:
#                 continue
#         else:
#             continue
        
#         snippet_tag = container.find("p", class_="Paragraph-sc-1iyax29-0 hdxKuG Hide-kg09cx-0 hWOBmI")
#         snippet_text = snippet_tag.get_text(strip=True) if snippet_tag else ""
        
#         date_tag = container.find("span", class_="sm-hide")
#         date_text = date_tag.get_text(strip=True) if date_tag else ""
        
#         articles.append({
#             "headline": headline_text,
#             "snippet": snippet_text,
#             "url": article_url,
#             "date": date_text,
#         })
#     return articles

# if __name__ == "__main__":
#     articles = scrape_real_estate_news(limit=2)
#     print("Scraped articles:")
#     print(articles)

import requests
from bs4 import BeautifulSoup

def scrape_real_estate_news(url="https://realestate.usnews.com/topics/subjects/real-estate", limit=15):
    # Fetch the webpage using requests
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page, status code: {response.status_code}")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    print("HTML preview:")
    print(soup.prettify()[:500])
    
    articles = []
    # Find article containers using the specific CSS classes
    containers = soup.find_all("div", class_="Box-w0dun1-0 MediaObject__Content-sc-19vl09d-3 bcZeaE lhdCWz")
    
    for idx, container in enumerate(containers):
        if idx >= limit:
            break
        
        # Find the headline element and extract the text and URL
        h3 = container.find("h3", class_="Heading-sc-1w5xk2o-0 kGRSaK story-headline")
        if h3:
            a_tag = h3.find("a")
            if a_tag:
                headline_text = a_tag.get_text(strip=True)
                article_url = a_tag.get("href", "")
                if article_url and article_url.startswith("/"):
                    article_url = "https://realestate.usnews.com" + article_url
            else:
                continue
        else:
            continue
        
        # Extract snippet and date if available
        snippet_tag = container.find("p", class_="Paragraph-sc-1iyax29-0 hdxKuG Hide-kg09cx-0 hWOBmI")
        snippet_text = snippet_tag.get_text(strip=True) if snippet_tag else ""
        
        date_tag = container.find("span", class_="sm-hide")
        date_text = date_tag.get_text(strip=True) if date_tag else ""
        
        articles.append({
            "headline": headline_text,
            "snippet": snippet_text,
            "url": article_url,
            "date": date_text,
        })
    
    return articles

if __name__ == "__main__":
    articles = scrape_real_estate_news(limit=2)
    print("Scraped articles:")
    print(articles)
