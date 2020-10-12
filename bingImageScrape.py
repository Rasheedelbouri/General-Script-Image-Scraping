# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:18:13 2020

@author: rashe
"""


#!/usr/bin/env python3
import requests
from requests.exceptions import InvalidSchema
import os
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
import time
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from PIL import Image
import io



def main(query, directory, numImgs=500):
    query= query.split()
    query='+'.join(query)
    os.mkdir(query)

    enc_query = urllib.parse.quote(query, safe='')
    url = 'https://bing.com/images/search?q={}&form=QBIRMH&sp=-1&pq={}&sc=1-5&cvid=65B33101F9344466A50723D24FE3D737&first=1&scenario=ImageBasicHover&safeSearch=on&count=150'.format(enc_query, enc_query)
    
        
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome('C:/Users/Rashe/Downloads/chromedriver/chromedriver.exe',chrome_options=options)
    driver.get(url)
    
    pause_time = 2

    results_start = 0
    img_urls = set()
    totalImgs = numImgs
    new_height=[]

    
    last_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height: 
            break
        last_height = new_height
        
        
    thumbnail_results = driver.find_elements_by_xpath("//a[contains(@class,'iusc')]")
    totalResults=len(thumbnail_results)

    for img in thumbnail_results[results_start:totalResults]:
        try:
            img.click()
            time.sleep(2)
            actual_images = driver.find_elements_by_css_selector('img')
            for actual_image in actual_images:
                img_count=len(img_urls)
        
                if img_count <= totalImgs:
                    if actual_image.get_attribute('src') and ('http' and 'pid') in actual_image.get_attribute('src') and not '.svg' in actual_image.get_attribute('src'):
                        img_urls.add(actual_image.get_attribute('src'))
                        print("image " + str(len(img_urls)) + " added")
                else:
                    break
        
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            continue
            
        
    print(f"Found: {img_count} image links")



    img_count=len(img_urls)
    print(f"Found: {img_count} image links")

    for i,ur in enumerate(img_urls):
        try:
            image_content = requests.get(ur).content
        
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
               
            file_path = os.path.join(query, str(i)+'.jpg')
                
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
        except InvalidSchema:
            continue

    return(url, query)
            
def scrape(query, numImgs): 
    url, query = main(query, query, numImgs)
    file = open(query+"/search_url.txt", "w")
    file.write(url)
    file.close()