# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from urllib.request import urlopen
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    
    mars_data = {}

    #Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    result = soup.find('div',class_="slide")
    title = result.find('div',class_='content_title').text
    news_p = result.find('div',class_='rollover_description_inner').text

    mars_data['title']=title
    mars_data['news_p']=news_p

    # JPL Mars Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = init_browser()
    browser.visit(url2)
    browser.find_by_css('.section_search').select('featured')
    browser.fill('search','Mars\n')
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html,'lxml')
    result = soup.find('li',class_='slide')
    image = result.find('a',class_='fancybox')
    image_url = image['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov'+image_url

    mars_data['featured_image_url']=featured_image_url

    # Mars Weather
    url3 = 'https://twitter.com/marswxreport'
    browser.visit(url3)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find('div',{"data-testid":"tweet"})
    result = result.find('div',class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    weather = result.text
    weather = weather.replace("InSight ","")
    weather = weather.replace("\n"," ")
    mars_weather = weather.replace("sol","Sol")

    mars_data['mars_weather']=mars_weather

    # Mars Facts
    url4 = 'https://space-facts.com/mars/'
    data = pd.read_html(url4)
    marsdata = pd.DataFrame(data[0])
    marsdata = marsdata.rename(columns={0:"Description",1: "Value"})
    mars_facts=marsdata.set_index('Description')
    mars_facts = mars_facts.to_dict()

    mars_data['mars_facts']=mars_facts

    # Mars Hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url5)
    soup = BeautifulSoup(response.text,'html.parser')
    result = soup.find_all('a',class_="itemLink product-item")
    hemisphere_image_urls = []
    for link in result:
        base_url = "https://astrogeology.usgs.gov/"
        final = link['href']
        url = base_url+final
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        title = soup.find('h2',class_="title").text
        result2 = soup.find_all('img',class_='wide-image')
        img_url = result2[0]['src']
        img_url = base_url+img_url
        img_url = img_url.replace("//","/")
        dict_mars = {'title':title,
                    'img_url':img_url}
        hemisphere_image_urls.append(dict_mars)
    
    mars_data['hemisphere_image_urls']=hemisphere_image_urls


    #Return
    return mars_data





