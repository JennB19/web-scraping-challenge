#!/usr/bin/env python
# coding: utf-8

# Mission to Mars - For this project, a web application is built to scrape data from various websites related to the Mission to Mars. Upon completioon, the information is displaye din a single html page.

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import pymongo
import pandas as pd
import time


def scrape_info():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Dictionary to story the scraped data
    mars_data = {}


# Executable path for Mac OS
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# In[3]:


# URL of page to be scraped
url = "https://mars.nasa.gov/news/"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[4]:


# This finds only the top or newest news story
news_story = soup.find("li", "slide")

# This scrapes the tile and teaser paragraph
for story in news_story:
    news_title = soup.find("div", "content_title").text
    news_para = soup.find("div", "article_teaser_body").text
    print(news_title)
    print(news_para)


# In[6]:


# This finds only the top or newest news story
news_story = soup.find("li", "slide")

# This scrapes the tile and teaser paragraph
for story in news_story:
    news_title = soup.find("div", "content_title").text
    news_para = soup.find("div", "article_teaser_body").text
    print(news_title)
    print(news_para)


# Visit the JPL featured space image web page. https://ww.jpl.nasa.gov/spaceimages/?search=&category=Mars
# Use Splinter to navigate the site and find the feature image URL and assign a url string to a vairable called feature_image_url. Find the image URL FOR THE FULL size .jpg image.
# Save a complet usrl string for this image.

# In[7]:


# URL of page to be scraped
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")


# This gets down to background-image:
background_image = soup.find("article")["style"]
print(background_image)

# Slice the string and add it to the rest of the path
featured_image_url = "https://www.jpl.nasa.gov" + background_image[23:-3]
print(featured_image_url)


# Visit Mars weather Twitter account at https://twiotter.com/marswxreport?land=en) and scrape the latest weather tweet. Save the tweet text for teh weather report as mars_weather.

# In[10]:


# URL of page to be scraped
url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[11]:


mars_weather = soup.find(
    "p", "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
).text
print(mars_weather)


# Visit the Mars facts site https://space-facts.com/mars/ and use Pandas to scrape the table that has facts about teh planet including diameter, mass, etc. Use Pandas to convert the data to a html string..

# In[12]:


# URL of page to be scraped
url = "http://space-facts.com/mars/"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[13]:


# read in any tables on the webpage
Mars_table = pd.read_html(url)


# In[14]:


# Name the columns
mars_df = Mars_table[1]
mars_df.columns = ["descriptor", "value"]
# Set descriptor as index
mars_df.set_index("descriptor", inplace=True)
mars_df


# In[15]:


# Convert dataframe to HTML table
mars_html_table = mars_df.to_html()
mars_html_table


# In[16]:


# Strip unwanted newlines (\n)
mars_html_table = mars_html_table.replace("\n", "")


# In[17]:


mars_html_table


# Visit the USGS AStrogeology site at https://astrolgeology.uysgs.gov/search/results?q=hemishpere+enhanced&k1=target&v1=Mars. Obtain high res images for each of Mar's hemispheres.

# In[18]:


# URL of page to be scraped
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[ ]:


products = soup.find("div", class_="collapsible results")
hemisphere = products.find_all("h3")

image_url_list = []
title_list = []

for record in hemisphere:
    try:
        # Capture the title
        title_list.append(record.text)
        # Click on the link
        browser.click_link_by_partial_text("Enhanced")
        # find the Original Image link on the new page
        downloads = browser.find_link_by_text("Sample").first
        link = downloads["href"]
        # Capture the sample image url
        image_url_list.append(link)
    except ElementDoesNotExist:
        print("Scraping Complete")

# use zip() to map values
titles_and_urls = zip(title_list, image_url_list)
# convert values to print as a set
titles_and_urls = set(titles_and_urls)

print(titles_and_urls)


# In[ ]:


print(title_list)


# In[ ]:


print(image_url_list)


# close the broswer after scraping
browser.quit()

# Return mars data dictionary

return mars_data

print(scrape_info)

