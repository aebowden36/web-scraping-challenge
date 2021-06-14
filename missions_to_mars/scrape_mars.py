from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime as dt
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

def mars_facts():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    browser.quit()
    return df.to_html(classes='table table-striped')

def hemispheres():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    for i in range(4):

        hemisphere = {}

        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample['href']

        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)

        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars News Site
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 

    try:
        title = soup.find('h2', class_='title').get_text()
        sample_element = soup.find('a', text='sample').get('href')
    except AttributeError:
        title = None
        sample_element = None

    hemispheres = {
        'title': title,
        'img_url': sample_element
    }

    return hemispheres

def scrape_all_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = scrape_news_info(browser)

    info = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': image(browser),
        'mars_facts': mars_facts(),
        'hemispheres': hemispheres(browser),
        'timestamp': dt.datetime.now()
    }

    browser.quit()
    return info

if __name__ =="__main__":
    print(scrape_all_info())