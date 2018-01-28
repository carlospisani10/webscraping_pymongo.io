
# coding: utf-8

# In[1]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import requests
import os
import pandas as pd
import time


# # ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."

# In[2]:
mars = {}
def scrape():

    browser = Browser('chrome', headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)


# In[3]:


    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[4]:


#collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
    title = soup.find("div", class_="content_title").a.text


# In[5]:


    paragraph = soup.find("div", class_="article_teaser_body").text


# In[6]:


    mars = {"Latest_News" : title,
            "Information": paragraph}


# # ### JPL Mars Space Images - Featured Image
# * Visit the url for JPL's Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# * Make sure to find the image url to the full size `.jpg` image.
# * Make sure to save a complete url string for this image.

# In[7]:


#run splinter browser
    browser = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)


# In[8]:


#click button for full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

# In[10]:


#click button for full image
    browser.click_link_by_partial_text('more info')
    time.sleep(2)


# In[11]:


#click button for full image
    browser.click_link_by_partial_text('.jpg')
    time.sleep(2)


# In[12]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find("img")['src']


# In[13]:


    mars["Feature_Photo"] = img_url


# # ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# ```

# In[14]:


    browser = Browser('chrome', headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)


# In[15]:


    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[16]:


    weather = soup.find("div", class_="js-tweet-text-container").text.strip()
    


# In[17]:


    mars["Current_Weather"] = weather


# # ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.

# In[18]:


    browser = Browser('chrome', headless=False)
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)


# In[19]:


    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[20]:


#collect the table. Assign the table to variables that you can reference later.
    table = pd.read_html(url)


# In[21]:


    table_df = pd.DataFrame(table[0])


# In[22]:


    table_df.columns = ["Stat", "Value"]
    table_df.set_index("Stat")


# In[23]:


    value_list = table_df["Value"]
    fact_list = table_df["Stat"]

    slim_facts = []
    for fact in fact_list:
        new_fact= fact.replace(" ", "_")
        slim_facts.append(new_fact)
    
# In[24]:


    fact_value = zip(slim_facts, value_list)


# In[25]:


    for fact, value in fact_value:
        mars[fact] = value


# In[ ]:





# # ### Mars Hemisperes
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# # # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]

# In[26]:


    hem_list = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    xpath1 = '//*[@id="wide-image"]/div/ul/li[1]/a'
    url_list = []
    hem_title= []


# In[27]:


    browser = Browser('chrome', headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)


# In[28]:


#loop attempt
    for hem in hem_list:
        browser.click_link_by_partial_text(hem)
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("div", class_="downloads").ul.li.a["href"]
   # get title
        text = soup.body.find('h2').text
    #append url and title to lists
        hem_title.append(text)
        url_list.append(img_url)
        browser.click_link_by_partial_text("Back")
        time.sleep(2)

        slim_title = []
    
    for title in hem_title:
        new_title= title.replace(" ", "_")
        slim_title.append(new_title)
    

# In[29]:


    hem_url = zip(slim_title, url_list)


# In[30]:


    for title, url in hem_url:
        mars[title] = url

    return mars
    

