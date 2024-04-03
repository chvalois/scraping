from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

from functions.functions import get_details

import re
import pandas as pd

from tqdm import tqdm
from datetime import datetime
import time
import random

user_agents = [
    # Add your list of user agents here
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

user_agent = random.choice(user_agents)

options = webdriver.ChromeOptions()

# rotate user agent
options.add_argument(f'user-agent={user_agent}')
# run in headless mode
options.add_argument('--headless=new')  # Runs Chrome in headless mode.
# disable the AutomationControlled feature of Blink rendering engine
options.add_argument('--disable-blink-features=AutomationControlled')
# disable pop-up blocking
options.add_argument('--disable-popup-blocking')
# start the browser window in maximized mode
options.add_argument('--start-maximized')
# disable extensions
options.add_argument('--disable-extensions')
# disable sandbox mode
options.add_argument('--no-sandbox')
# disable shared memory usage
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')

#options.add_argument("--window-size=1920,1080")
#options.add_argument('--allow-running-insecure-content')
#options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
#options.add_argument("--disable-gpu")

#ervice = Service(executable_path='/usr/local/bin/chrome-headless-shell-linux64/chrome-headless-shell')
#service = Service(executable_path='/usr/local/bin/chromedriver-win64/chromedriver.exe')
#driver = webdriver.Chrome(service=service, options=options)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Change the property value of the navigator for webdriver to undefined
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

stealth(driver,
        languages=["fr-FR", "fr"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

def vpn_init():

    for i in range(2):
        try:
            settings = initialize_VPN(stored_settings=1)    # ['complete rotation'] for complete rotation
            print('VPN Initialization Succeeded')
        except:   
            settings = None
            print('VPN Initialization Failed')
            
        return settings

def vpn_rotate(settings):
        
    try:
        rotate_VPN(settings)
    except:
        pass

def daily_scraping(region_dept, use_vpn=False): 

    if use_vpn == True:
        settings=vpn_init()

    scraping_dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    today_dt = datetime.now().strftime("%d/%m/%Y")

    region_dept_alphanum = re.sub('[^A-Za-z0-9]+', '', region_dept)
    start_url = f'https://www.superimmo.com/achat/{region_dept}?option%5B%5D=old_build&sort=created_at'

    driver.get(start_url)
    time.sleep(5)

    # Wait for page to load
    while driver.execute_script("return document.readyState") != "complete":
        pass
    driver.save_screenshot('start_url.png')

    try:
        button = driver.find_element(By.XPATH, '//*[@id="tarteaucitronPersonalize2"]')
        button.click()
    except:
        pass

    max_pages = int(driver.find_element(By.XPATH, '//*[@id="pjax-container"]/div[2]/nav/ul/li[10]/a').text)

    df = pd.DataFrame()

    ind = 0

    for page in tqdm(range(1, max_pages)):

        if use_vpn == True:
            vpn_rotate(settings)

        if page == 1:
            page = 0
        pages_url = f'https://www.superimmo.com/achat/{region_dept}/p/{page}?option%5B%5D=old_build&sort=created_at'
        driver.get(pages_url)

        last_published = driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/section/article[1]/section/div[2]/div[3]/small').text[-10:]

        if last_published != today_dt:
            break

        for i in tqdm(range(1, 16), leave = False):
            
            driver.get(pages_url)
            url = driver.find_element(By.XPATH, f'//*[@id="pjax-container"]/section/article[{i}]/section/div[5]/p/a').get_attribute("href")
            price, surface, nb_pieces, nb_chambres, location, prix_m2, date_publication, tag_1, tag_2, tag_3, description, tags, images_url = get_details(url, driver)

            new_row = pd.DataFrame({'url': url, 'price': price, 'surface': surface, 'nb_pieces': nb_pieces,
                                            'nb_chambres': nb_chambres, 'lieu': location, 'prix_m2': prix_m2,
                                            'date_publication': date_publication, 'tag_1': tag_1, 'tag_2': tag_2,
                                            'tag_3': tag_3, 'description': description, 
                                            'tags': [tags], 'images_url': [images_url]})

            df = pd.concat([df, new_row], ignore_index = True)

        try:
            df.to_csv(f'files/df_{region_dept_alphanum}_{scraping_dt}.csv', sep = ";")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


    print(df.head())

    if use_vpn == 1:
        terminate_VPN(instructions=None)

daily_scraping('corse/corse-du-sud')
