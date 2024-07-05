from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import pandas as pd
import numpy as np

from tqdm import tqdm
import time

def get_details(url, driver):
    driver.get(url)
    
    price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication = '', '', '', '', '', '', ''
    tag_1, tag_2, tag_3, description = '', '', '', ''
    images_url = [None] * 10
    tags = [None] * 20


    try:
        price = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/section[1]/table/tbody/tr/td[1]').text
        price = re.findall(r'Prix de vente : (\d* *\d+ \d+) €', price)[0]
    except:
        pass

    try:
        surface = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[1]').text
        surface = re.findall(r'(\d+)* m²', surface)[0]
    except:
        pass

    try:
        nb_pieces = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[2]/span[1]').text
        nb_pieces = re.findall(r'(\d+)', nb_pieces)[0]
    except:
        pass

    try:
        nb_chambres = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[3]/span[1]').text
        nb_chambres = re.findall(r'(\d+)', nb_chambres)[0]
    except:
        pass

    
    try:
        location = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[4]').text
    except:
        try:
            location = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[3]').text
            if re.match(r'.*\d{5}', location) is None:
                location = ''
        except:
            pass

    try:
        prix_m2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/ul/li[1]').text
        prix_m2 = re.findall(r'(\d* *\d+) €\/m²', prix_m2)[0]
    except:
        pass

    try:
        date_publication = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]').text
        date_publication = re.findall(r'Publiée le (\d{2}/\d{2}/\d{4})', date_publication)
    except:
        pass

    try:
        tag_1 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/ul/li[2]').text
        tag_2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/ul/li[3]').text
    except:
        pass

    try:
        tag_3 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[3]/p').text
    except:
        pass


    for i in range(1, 11):
        for j in range(1, 3):
            try:
                tag = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[2]/section[2]/table/tbody/tr[{i}]/td[{j}]').text
                tags[(i-1) * 2 + j - 1] = tag
            except:
                pass

    try:
        description = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/p').text
    except:
        pass
    
    try:
        nb_images = int(driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[1]/div[1]/span').text)
        for img in range(1, nb_images + 1):
            url = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[1]/div[1]/div[1]/div[2]/div[{img}]/span/img').get_attribute("src")
            images_url[img - 1] = url
    except:
        pass
    
    return price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication, tag_1, tag_2, tag_3, description, tags, images_url