# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import requests
import os
import pandas as pd

mars = {}
def scrape():

    ### NASA Mars News

    browser = Browser('chrome', headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("div", class_="content_title").text
    paragraph = soup.find("div", class_="article_teaser_body").text

    mars = {"Latest News" : title,
    "Information": paragraph}

    ### JPL Mars Space Images - Featured Image

    #run splinter browser
    browser = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #click button for full image
    browser.click_link_by_partial_text('FULL IMAGE')

    #click button for full image
    browser.click_link_by_partial_text('more info')

    #parse the second column for the image URL
    # Design an XPATH selector to grab the "Mars in natural color in 2007" image on the right
    #IMPORTANT: THE XPATH CHANGES, the li index is either 5 or 7. IF error happens use other number
    xpath = '//*[@id="secondary_column"]/aside[1]/ul/li[5]/div/p/a'

    # Use splinter to Click the "Mars in natural color in 2007" image 
    # to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find("img")['src']

    mars["Feature Photo"] = img_url

    ### Mars Weather

    browser = Browser('chrome', headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather = soup.find("div", class_="js-tweet-text-container").text
    mars["Current Weather"] = weather

    ### Mars Facts

    browser = Browser('chrome', headless=False)
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #collect the table. Assign the table to variables that you can reference later.
    table = pd.read_html(url)

    table_df = pd.DataFrame(table[0])
    table_df.columns = ["Stat", "Value"]
    table_df.set_index("Stat")
    value_list = table_df["Value"]
    fact_list = table_df["Stat"]

    fact_value = zip(fact_list, value_list)
    for fact, value in fact_value:
        mars[fact] = value

    ### Mars Hemisperes

    hem_list = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    xpath1 = '//*[@id="wide-image"]/div/ul/li[1]/a'
    url_list = []
    hem_title= []

    browser = Browser('chrome', headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #loop attempt
    for hem in hem_list:
        browser.click_link_by_partial_text(hem)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("div", class_="downloads").ul.li.a["href"]
        # get title
        text = soup.body.find('h2').text
        #append url and title to lists
        hem_title.append(text)
        url_list.append(img_url)
        browser.click_link_by_partial_text("Back")
    
    hem_url = zip(hem_title, url_list)
    for title, url in hem_url:
        mars[title] = url
    
    return mars
    

