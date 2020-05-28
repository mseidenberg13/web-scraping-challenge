from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time



def init_browser():
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    #Scrape News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title= soup.find_all('div', class_= "content_title")[1].text
    news_p = soup.find('div', class_="article_teaser_body").text

    #Scrape Featured image
    nasa_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    image_path = image_soup.find('article', class_='carousel_item')
    footer = image_path.find('footer')
    a_footer = footer.find('a')
    path = a_footer['data-fancybox-href']
    featured_image_url = (nasa_url + path)

    #Scrape twitter weather
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter)
    time.sleep(1)
    twitter_html = browser.html
    weather_soup = bs(twitter_html, 'html.parser')
    weather_report = weather_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[27].text

    #Scrape facts table
    facts_url = 'https://space-facts.com/mars/'
    facts_tables = pd.read_html(facts_url)
    facts_df = facts_tables[0]
    facts_df.columns=["Factor", "Fact"]
    facts_df.set_index("Factor", inplace=True)

    facts_html_table = facts_df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')

    #Scrape mars hemisphere images
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    cerberus_html = browser.html
    cerberus_soup = bs(cerberus_html, 'html.parser')

    cerberus_link = cerberus_soup.find('div', class_='downloads')
    link = cerberus_link.find('a')
    cerberus_url = link['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    schiaparelli_html = browser.html
    schiaparelli_soup = bs(schiaparelli_html, 'html.parser')

    schiaparelli_link = schiaparelli_soup.find('div', class_='downloads')
    link = schiaparelli_link.find('a')
    schiaparelli_url = link['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    syrtis_html = browser.html
    syrtis_soup = bs(syrtis_html, 'html.parser')

    syrtis_link = syrtis_soup.find('div', class_='downloads')
    link = syrtis_link.find('a')
    syrtis_url = link['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    valles_html = browser.html
    valles_soup = bs(valles_html, 'html.parser')

    valles_link = valles_soup.find('div', class_='downloads')
    link = valles_link.find('a')
    valles_url = link['href']

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": valles_url},
        {"title": "Cerberus Hemisphere", "img_url": cerberus_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_url},
    ]

    mars_data = { 
        'news_headline': news_title,
        'news_paragraph':  news_p,
        'featured_image': featured_image_url,
        'mars_weather': weather_report,
        'facts_table': facts_html_table,
        "va_title": "Valles Marineris Hemisphere", "va_img_url": valles_url,
        "ce_title": "Cerberus Hemisphere", "ce_img_url": cerberus_url,
        "sc_title": "Schiaparelli Marineris Hemisphere", "sc_img_url": schiaparelli_url,
        "sy_title": "Syrtis Major Hemisphere", "sy_img_url": syrtis_url
    }

    browser.quit()
    return mars_data