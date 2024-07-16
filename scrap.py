from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


#function to scroll
def scroll(number_of_time):
    for i in range(number_of_time):
        driver.execute_script("window.scrollBy(0, 4200)")
        #setting sleep/waiting time for the page to load
        time.sleep(1)


#Defining the website and maximizing the window

def data_collection():
    global driver
    # Set the path to the ChromeDriver executable
    chromedriver_path = r"E:/1/chromedriver-win64/chromedriver.exe"

    # Create a service object for ChromeDriver
    service = Service(chromedriver_path)

    # Create Chrome options
    chrome_options = Options()
    # Add any necessary options (optional)
    # chrome_options.add_argument("--headless")

    # Initialize the WebDriver with the service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    website='https://botpenguin.com/'
    driver.get(website)
    driver.maximize_window()

    #calling the scroll function to get all the elements
    scroll(5)

    #Driver elements for scrapping contents from the page
    passage1=driver.find_elements(By.XPATH,value='//div[@class="col-md-6 col-sm-12 first-banner-content"]')
    passage2=driver.find_elements(By.XPATH,value='//div[@class="top-banner"]')
    passage3=driver.find_elements(By.XPATH,value='//div[@class="container"]')
    passage4=driver.find_elements(By.XPATH,value='//div[@class="col-lg-6 col-md-6 col-sm-12 banner-content"]')
    passage5=driver.find_elements(By.XPATH,value='//div[@class="content"]')

    #trimming unwanted parts
    passage3=passage3[1:-3]
    #Defining empty list for storing the contents fetched from each driver elements
    doc=[]

    #Custom for loop to sort and save the data scrapped in proper order
    for i in range(8):
        doc.append(passage3[i].text)
        if i==1:
            doc.append(passage4[0].text)
        if i<6:
            doc.append(passage2[i].text)
        if i==1:
            doc.append(passage5[0].text)
            
    #creating a varibale where the entire context will be saved        
    corpus=" ".join(doc)
    driver.close()
    return corpus