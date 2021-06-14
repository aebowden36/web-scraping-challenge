from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_news_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    try:
        #find initial parent element
        initial = soup.select_one('div.list_text')
        # Get the news title
        news_title = initial.find('div', class_='content_title').get_text
        # Get the news paragraph text
        news_p = initial.find('div', class_='article_teaser_body').get_text
    except AttributeError:
        return None, None

    #store data in a dictionary
    mars_data = {"news title":news_title,"news paragraph":news_p}
    
    # Quit the browser after scraping
    browser.quit()
    return mars_data

def image():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        image_url = soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    featured_image_url = f'https://spaceimages-mars.com/{image_url}'
    browser.quit()