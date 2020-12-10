
#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    

    ## NASA Mars News

    # URL of page to be scraped
    url='https://mars.nasa.gov/'
    response = requests.get(url)

    # creating the soup object
    soup = bs(response.text, "html.parser")

    # Search for news titles
    item_list_ul = soup.find_all('div', class_='list_text')[0]

    news_title=item_list_ul.find('h3',class_ = 'title').text


    ## JPL Mars Space Images - Featured Image
    browser = init_browser()
    # URL of page to be scraped
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' 
    browser.visit(url)
    html = browser.html

    # Creating the soup object
    soup = bs(html, 'html.parser')

    # Click through to find full image
    full_image_button = browser.links.find_by_partial_text("FULL IMAGE")
    full_image_button.click()

    more_info_button = browser.links.find_by_partial_text("more info")
    more_info_button.click()

    new_page = bs(browser.html,'html.parser')

    featured_image_url = f"https://www.jpl.nasa.gov{new_page.find('img',class_ = 'main_image')['src']}"
    
    browser.quit()

    ## Mars Facts

    # URL to be scraped
    url= 'https://space-facts.com/mars/'

    #defining table
    table = pd.read_html(url)

    #asking for the first table found 
    factsdf = table[0]
    factsdf.columns=["Properties", "Values"]
    factsdf

    # Convert table to html
    mars_facts = factsdf.to_html(index=False, header=False)
    
 
    
    ## Mars Hemispheres

    browser = init_browser()

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemisphere_image_urls = []

    # creating the List of the Hemispheres
    for x in range(0,4):
        hemisphere = {}
        
        #Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[x].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Quit Browser
        browser.back()

    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "featured_image": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_image_urls
    }

    # Return results
    return mars_data


