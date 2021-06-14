from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set executable path and initialize browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_news_info(browser):
    # Visit Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    try:
        #find initial parent element
        initial = soup.select_one('div.list_text')
        # Get the news title
        news_title = initial.find('div', class_='content_title').get_text()
        # Get the news paragraph text
        news_p = initial.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

def image(browser):
    # Visit Image Site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    full_image = browser.find_by_tag('button')[1]
    full_image.click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        img_url = soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    featured_image_url = f'https://spaceimages-mars.com/{img_url}'
    return featured_image_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes='table table-striped')

def hemispheres(browser):
    # Visit Mars News Site
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemi_img_urls = []

    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemisphere = {}

        browser.find_by_css('a.product-item img')[i].click()

        sample = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample['href']

        hemisphere['title'] = browser.find_by_css('h2.title').text

        hemi_img_urls.append(hemisphere)

        browser.back()
    return hemi_img_urls

def scrape_hemisphere(html_text): 

    soup = bs(html_text, "html.parser") 

    try:
        title = soup.find('h2', class_='title').get_text()
        sample_element = soup.find('a', text='Sample').get('href')
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