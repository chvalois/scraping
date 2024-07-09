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

def find_property(driver, x_path, surface, nb_pieces, nb_chambres, location):
    """
    Description:
    This function returns property values of the ad depending on the xpath

    Args:
    - x_path: x_path of the block of code
    - surface: existing value in surface
    - nb_pieces: existing value in nb_pieces
    - nb_chambres: existing value in nb_chambres
    - location: existing value in location

    Returns:
    - surface: new value in surface if the xpath corresponds to a surface property
    - nb_pieces: new value in nb_pieces if the xpath corresponds to a nb_pieces property
    - nb_chambres: new value in nb_chambres if the xpath corresponds to a nb_chambres property
    - location: new value in location if the xpath corresponds to a location property

    Raises:
    - None
    """

    property = driver.find_element(By.XPATH, x_path).text

    if re.search(r"m²", property):
        surface = re.findall(r'(\d+)* m²', property)[0]
        surface = int(surface.replace(" ", ""))
    elif re.search(r"pièce", property):
        nb_pieces = re.findall(r'(\d+)', property)[0]
        nb_pieces = int(nb_pieces.replace(" ", ""))
    elif re.search(r"chambre", property):
        nb_chambres = re.findall(r'(\d+)', property)[0]
        nb_chambres = int(nb_chambres.replace(" ", ""))
    elif re.search(r"([\wéè]+)\s*\((\d+)\)", property):
        location = property

    return surface, nb_pieces, nb_chambres, location


def get_details(url, driver):
    """
    Description:
    This function returns values describing the ad that is being scraped

    Args:
    - url: url of the page being scraped
    - driver: driver used to do the scraping

    Returns:
    - price: official sale price of the house or apartment
    - surface: official surface
    - nb_pieces: number of rooms
    - nb_chambres: number of bedrooms
    - location: location (city + zipcode)
    - prix_m2: price per square meter
    - date_publication: publishing date
    - tag_1: main tag 1
    - tag_2: main tag 2
    - tag_3: main tag 3
    - description: description of the ad
    - tags: array of tags as seen in the table of the ad description
    - images_url: url of the images of the house or apartment

    Raises:
    - Generic Exception
    """

    driver.get(url)
    
    price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication = '', '', '', '', '', '', ''
    tag_1, tag_2, tag_3, description = '', '', '', ''
    images_url = [None] * 10
    tags = [None] * 20

    # Recherche du prix de vente
    try:
        price = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/section[1]/table/tbody/tr/td[1]').text
        price = re.findall(r'Prix de vente : (\d* *\d+ \d+) €', price)[0]
        price = int(price.replace(" ", ""))
    except:
        pass

    # Etude de chaque bloc en-dessous de l'image principale de l'annonce
    for xpath in ['/html/body/main/div[2]/div[1]/div[2]/div[2]/div/h1/div/div[1]',
                  '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[1]',
                  '/html/body/main/div[2]/div[1]/div[2]/div[2]/div/h1/div/div[2]',
                  '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[2]',
                  '/html/body/main/div[2]/div[1]/div[2]/div[2]/div/h1/div/div[3]',
                  '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[3]',
                  '/html/body/main/div[2]/div[1]/div[2]/div[2]/div/h1/div/div[4]',
                  '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[4]',
                  '/html/body/main/div[2]/div[1]/div[2]/div[2]/div/h1/div/div[5]',
                  '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[5]',
                ]:  

        try:
            surface, nb_pieces, nb_chambres, location = find_property(driver, xpath, surface, nb_pieces, nb_chambres, location)        
        except:
            pass
        
    # Recherche des autres propriétés
    try:
        prix_m2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/ul/li[1]').text
        if re.search(r'(\d* *\d+) €\/m²', prix_m2):
            prix_m2 = re.findall(r'(\d* *\d+) €\/m²', prix_m2)[0]
            prix_m2 = int(prix_m2.replace(" ", ""))
        else:
            prix_m2 = ''
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
            image_url = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[1]/div[1]/div[1]/div[2]/div[{img}]/span/img').get_attribute("src")
            images_url[img - 1] = image_url
    except:
        pass

 
    try:
        print(
            "URL:", url, "\n",
            "Price:", price, "\n",  
            "Surface:", surface, "\n", 
            "Nb pieces:", nb_pieces, "\n", 
            "Nb chambres:", nb_chambres, "\n", 
            "Location:", location, "\n", 
            "Prix m2:", prix_m2, "\n", 
            "Date Publi:", date_publication, "\n", 
            "Tag 1:", tag_1, "\n", 
            "Tag 2:", tag_2, "\n", 
            "Tag 3:", tag_3, "\n", 
            "Description:", description, "\n", 
            "Tags:", tags, "\n", 
            "Url Images:", images_url, "\n"
        )  

        return price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication, tag_1, tag_2, tag_3, description, tags, images_url
    
    except Exception as e:
        print(e)





"""
def get_details(url, driver):
    driver.get(url)
    
    price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication = '', '', '', '', '', '', ''
    tag_1, tag_2, tag_3, description = '', '', '', ''
    images_url = [None] * 10
    tags = [None] * 20


    try:
        price = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/section[1]/table/tbody/tr/td[1]').text
        price = re.findall(r'Prix de vente : (\d* *\d+ \d+) €', price)[0]
        price = int(price.replace(" ", ""))
    except:
        pass

    try:
        surface = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[1]').text
        surface = re.findall(r'(\d+)* m²', surface)[0]
        surface = int(surface.replace(" ", ""))
    except:
        pass

    try:
        nb_pieces = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[2]/span[1]').text
        nb_pieces = re.findall(r'(\d+)', nb_pieces)[0]
        nb_pieces = int(nb_pieces.replace(" ", ""))
    except:
        pass

    try:
        nb_chambres = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div[2]/div/h1/div/div[3]/span[1]').text
        nb_chambres = re.findall(r'(\d+)', nb_chambres)[0]
        nb_chambres = int(nb_chambres.replace(" ", ""))
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
        prix_m2 = int(prix_m2.replace(" ", ""))
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
    """