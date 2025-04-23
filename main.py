from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import sys
import re

import argparse

# Set your Chrome user data path (adjust this!)
user_data_dir = r"C:\\Users\\LianLie 1\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Profile 6"  # or "Profile 1", etc.


def links_scraper(target, output):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    url = target
    output_file = output
    # domain = "parpol.ahu.go.id"

    try:
        driver.get(url)
        print(f"[INFO] URL: {url}")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html_content = driver.page_source
        print(f"[INFO] HTML Content: {html_content}")
        lines = html_content.splitlines()
        link_regex = re.compile(r'href="([^"]+)"')
        parsed_links = []
        for line_num, line in enumerate(lines, start=1):
            matches = link_regex.findall(line)
            if matches:
                for link in matches:
                    parsed_links.append((line_num, link))

        with open(output_file, "w") as f:
            for line_number, link in parsed_links:
                f.write(f"Line {line_number}: {link}\n")
        print(f"Parsed {len(parsed_links)} links. Output saved to '{output_file}'.")
    except Exception as e:
        print(f"[INFO] HTML Content: {html_content}")
        print(f"Error: {e}")
        driver.quit()
        sys.exit("Exiting...")
    input("Press Enter to exit and close browser...")
    driver.quit()

# driver = webdriver.Chrome(options=chrome_options)
def scrape_page(target):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    # https://www.bumn.go.id/portofolio/brand?page=1
    # driver.get(f"https://shopee.co.id/search_user?keyword={keyword}")  # This will carry your logged-in session
    # loops the page until the end of the page
    loops = 1
    
    # Define XPath Shopee
    # xpath1 = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]'
    # xpath_loop = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/a/div[2]'
    # total_produk = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[1]/div/div[1]/span'
    # penilaian = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[2]/div/div[1]/span'
    # persentase_chat_dibalas = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[3]/div/div[1]/span'
    
    
    # Define XPath BUMN Page
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[loops]/div/a
    
    # xpath1 = '/html/body/div[1]/section[2]/div/div[1]'
    # xpath_loop = '/html/body/div[1]/section[2]/div/div[1]/div[{loop}]/div/a'
    
    # XPATH Lembaga Kementrian 
    # /html/body/section/div/div[2]/div/div/table/tbody/tr[1]/td[4]/a
    # /html/body/section/div/div[2]/div/div/table/tbody/tr[2]/td[4]/a
    
    xpath1 = '/html/body/section/div/div[2]/div/div/table/tbody'
    xpath_loop = '/html/body/section/div/div[2]/div/div/table/tbody/tr[{loop}]/td[4]/a'
    # Wait for the container to appear
    try:
        driver.get(f"{target}")  # This will carry your logged-in session
        wait.until(EC.presence_of_element_located((By.XPATH, xpath1)))
        # Count Child divs under xpath1
        parent = driver.find_element(By.XPATH, xpath1)
        # child_divs = parent.find_elements(By.XPATH, "./div")
        child_divs = parent.find_elements(By.XPATH, "./tr")
        total_items = len(child_divs)
        print(f"[INFO] Total Items Found: ", total_items)
        # Loop through and extract values using xpath_loop
        try:
            for i in range(1, total_items + 1):
                xpath = xpath_loop.format(loop=i)
                xpath_link_web = xpath_loop.format(loop=i)
                # Untuk Shopee
                # xpath_penilaian = penilaian.format(loop=i)
                # xpath_persentase_chat_dibalas = persentase_chat_dibalas.format(loop=i)
                try:
                    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    element_link_web = wait.until(EC.presence_of_element_located((By.XPATH, xpath_link_web)))
                    print(f"Item {i}: {element.text}, links: {element_link_web.get_attribute('href')}")
                    # with open("list_toko", "w") as f:
                except Exception as e:
                    print(f"[WARN] Element {i} not found or failed to load. Error: {e}")
                    # Prevent browser from closing for review/debug
                    input("Press Enter to exit and close browser...")
                    driver.quit()
        except Exception as e:
            print(f"[WARN] Element {i} not found or failed to load. Error: {e}")
            # Prevent browser from closing for review/debug
            input("Press Enter to exit and close browser...")
            driver.quit()
    except Exception as e:
        print("No Result Founds")
        # sys.exit("Exiting....")
        input("Press Enter to exit and close browser...")
        driver.quit()
    driver.quit()

def scrape_w_param_loop(target):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    # https://www.bumn.go.id/portofolio/brand?page=1
    # driver.get(f"https://shopee.co.id/search_user?keyword={keyword}")  # This will carry your logged-in session
    # loops the page until the end of the page
    loops = 1
    
    # Define XPath Shopee
    # xpath1 = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]'
    # xpath_loop = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/a/div[2]'
    # total_produk = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[1]/div/div[1]/span'
    # penilaian = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[2]/div/div[1]/span'
    # persentase_chat_dibalas = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[3]/div/div[1]/span'
    
    
    # Define XPath BUMN Page
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[1]/div/a
    # /html/body/div[1]/section[2]/div/div[1]/div[loops]/div/a
    
    # xpath1 = '/html/body/div[1]/section[2]/div/div[1]'
    # xpath_loop = '/html/body/div[1]/section[2]/div/div[1]/div[{loop}]/div/a'
    
    # XPATH Lembaga Kementrian 
    # /html/body/section/div/div[2]/div/div/table/tbody/tr[1]/td[4]/a
    # /html/body/section/div/div[2]/div/div/table/tbody/tr[2]/td[4]/a
    
    xpath1 = '/html/body/section/div/div[2]/div/div/table/tbody'
    xpath_loop = '/html/body/section/div/div[2]/div/div/table/tbody/tr[{loop}]/td[4]/a'
    
    while loops <= 8:
        driver.get(f"https://www.bumn.go.id/portofolio/brand?page={loops}")  # This will carry your logged-in session
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath1)))
            # Count Child divs under xpath1
            parent = driver.find_element(By.XPATH, xpath1)
            child_divs = parent.find_elements(By.XPATH, "./div")
            total_items = len(child_divs)
            print(f"[INFO] Total Items Found: ", total_items)
            # Loop through and extract values using xpath_loop
            try:
                for i in range(1, total_items + 1):
                    xpath = xpath_loop.format(loop=i)
                    xpath_link_web = xpath_loop.format(loop=i)
                    
                    # Untuk Shopee
                    # xpath_penilaian = penilaian.format(loop=i)
                    # xpath_persentase_chat_dibalas = persentase_chat_dibalas.format(loop=i)
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        element_link_web = wait.until(EC.presence_of_element_located((By.XPATH, xpath_link_web)))
                    
                        #    Untuk Shopee
                        # element_total_produk = wait.until(EC.presence_of_element_located((By.XPATH, xpath_total_produk)))
                        # element_penilaian = wait.until(EC.presence_of_element_located((By.XPATH, xpath_penilaian)))
                        # element_persentase_chat_dibalas = wait.until(EC.presence_of_element_located((By.XPATH, xpath_persentase_chat_dibalas)))
                        # print(f"Item {i}: {element.text} (total_produk: {element_total_produk.text}, penilaian: {element_penilaian.text}, persentase chat dibalas: {element_persentase_chat_dibalas.text})")
                        print(f"Item {i}: {element.text}, links: {element_link_web.get_attribute('href')}")
                        # with open("list_toko", "w") as f:
                    except Exception as e:
                        print(f"[WARN] Element {i} not found or failed to load. Error: {e}")
                # Prevent browser from closing for review/debug
                input("Press Enter to exit and close browser...")
                loops += 1
            except Exception as e:
                print(f"[WARN] Element {i} not found or failed to load. Error: {e}")
                # Prevent browser from closing for review/debug
                input("Press Enter to exit and close browser...")
                driver.quit()
        except Exception as e:
            print("No Result Founds")
            # sys.exit("Exiting....")
            input("Press Enter to exit and close browser...")
            driver.quit()
    driver.quit()


def parse_args():
    parser = argparse.ArgumentParser(description="This Is Shopee Store Scraper With Selenium")
    parser.add_argument("--wordlist", type=str)
    parser.add_argument("--target", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    target = args.target
    # with open(args.wordlist, "r") as f:
    #     keyword = f.read()
    #     print(f"{keyword}")
    # sys.exit()

    scrape_page(target)
    # links_scraper(target, "output.txt")
