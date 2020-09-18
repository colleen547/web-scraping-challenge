#!/usr/bin/env python
# coding: utf-8

# # *Mission to Mars*

# ### Web Scraping

# ### *NASA Mars News*


import os
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape_info():

    browser = Browser('chrome')

    mars = {}

    # Access the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"

    # Using Beautiful Soup and assign parser to write webpage data into html
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")


    news_title = soup.find_all("div",class_="content_title")[1].text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    mars["news_title"]=news_title
    mars["news_paragraph"]=news_paragraph

    ### *JPL Mars Space Images - Featured Image*

    # Visit the "jpl.nasa.gov" web page
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.find_link_by_partial_text('more info').click()

    # Get the image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("figure", class_="lede").a.img["src"]
    full_img_url = "https://www.jpl.nasa.gov" + img_url
    print(full_img_url)
    mars["feature_image"]=full_img_url
    mars

    ### *Mars Facts*

    url_facts = "https://space-facts.com/mars/"

    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table
    mars["fact"]=mars_html_table

    #### *Mars Hemispheres*

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)    
    time.sleep(5)       
    usgs_soup = bs(browser.html, 'html.parser')
    headers = []
    titles = usgs_soup.find_all('h3')  
    time.sleep(5)
    for title in titles: 
        headers.append(title.text)
    images = []
    count = 0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count = count+1
    hemisphere_image_urls = []  #initialize empty list to collect titles
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1

    # closeBrowser(browser)
    browser.back()
    time.sleep(1)
    mars["hemispheres"]=hemisphere_image_urls

    return mars

if __name__ == "__main__":
    print(scrape_info())