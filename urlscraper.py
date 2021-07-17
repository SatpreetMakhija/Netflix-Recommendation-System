from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time
import csv
from bs4 import BeautifulSoup as bs4

def main():
    driver_path = './chromedriver'
    driver = webdriver.Chrome(driver_path)

    websiteLink = 'https://flixable.com/?min-rating=0&min-year=1920&max-year=2022&order=title#filterForm'
    driver.get(websiteLink)
    time.sleep(2)
    
   
    ## scrape data
    # finalData = scrapeData(driver)
    scrapeData(driver)

    time.sleep(200)
    driver.quit()

def scrapeData(driver):
    screen_height = driver.execute_script("return window.screen.height;") 
    scroll_pause_time = 1
    i =1
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if scroll_height == 733328:
            break
        # if (screen_height)*i > scroll_height:
        #     break
        # try:
        #    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        #    i += 1
        #    time.sleep(scroll_pause_time)
        #    scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # #    if (screen_height)*i > scroll_height:
        # #        break
        # except:
        #     pass

    urls = []
    soup = bs4(driver.page_source, "html.parser")
    baseURL = "https://flixable.com"
    for movieCard in soup.find_all(class_ = "card-body"):
    
        a_tag = movieCard.find("a")
        if a_tag:
            link = a_tag.attrs["href"]
            url = baseURL + link
            urls.append([url])

    with open("./urls.csv", "w") as file:
        csvWriter = csv.writer(file)
        csvWriter.writerows(urls)
    print("completed")

   



main()