def scrape():

    # Dependencies
    from bs4 import BeautifulSoup as bs
    import os
    import pymongo # to export to mongo
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from splinter import Browser

    MarsFacts={"Latest News":"", "Space Featured Image":"", "Current Weather":"","Facts":"","Hemispheres":"" }
    # soupify News
    url='https://mars.nasa.gov/news/'

    executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    titleWhole = soup.find('div', class_='content_title')
    title=titleWhole.find('a').text
    paragraph = soup.find('div', class_='article_teaser_body').text


  
    news={"Title": title, "Summary":paragraph}
    MarsFacts["Latest News"]=news
    
    # soupify image
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    feature = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
    article=feature.find('article', class_='carousel_item')
    a=article.find('a')
    picture=a['data-fancybox-href']
    MarsFacts["Space Featured Image"]='https://www.jpl.nasa.gov' +picture
    
    #weather
    url='https://twitter.com/marswxreport?lang=en'
    executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    p= soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather=p.text
    MarsFacts["Current Weather"]=mars_weather
    
    #     table
    url = "https://space-facts.com/mars/"
    RawDataDF = pd.read_html(url)
    RawDataDF=RawDataDF[0]
    RawDataDF = RawDataDF.rename( columns={0: "Fact", 1:"Value"}).reset_index()
    MarsFactsDF=RawDataDF[["Fact","Value"]]
    html = MarsFactsDF.to_html()
    cleanHTML=html.replace('\n', '')
    MarsFacts["Facts"]=cleanHTML

    
#     images

    executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #2. Find the element with the small thumb that I need to click. get the picture name from there, and the address to the full picture, stored under src.

    Allpictures = soup.find_all('a', class_='itemLink product-item')

    images=[]
    individualDic={"title":'', "Image Url":""}

    images=[]
    for pictures in Allpictures:

        desc=pictures.find('h3')
        #grab the description and addit to the dictionary
        if desc != None:
            individualDic["title"]=desc.text
            insideURL="https://astrogeology.usgs.gov"+pictures["href"]
            #this gives me the list of urls where I need to go to get the hight resolution image. I need to loop though each.     


            browser.visit(insideURL)
            html2 = browser.html
            soup2 = bs(html2, 'html.parser')
            img=soup2.find('img', class_="thumb")
            FinalLoc="https://astrogeology.usgs.gov"+img["src"]
            individualDic["Image Url"]=FinalLoc
            images.append(individualDic)
            individualDic={}
    MarsFacts["Hemispheres"]=images 
    
    return MarsFacts

