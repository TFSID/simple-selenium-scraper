from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import sys

import argparse

# Set your Chrome user data path (adjust this!)
user_data_dir = r"C:\\Users\\LianLie 1\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Profile 6"  # or "Profile 1", etc.

# driver = webdriver.Chrome(options=chrome_options)
def scrape_username_toko(keyword):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get(f"https://shopee.co.id/search_user?keyword={keyword}")  # This will carry your logged-in session

    # Define XPath
    xpath1 = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]'
    xpath_loop = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/a/div[2]'
    total_produk = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[1]/div/div[1]/span'
    penilaian = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[2]/div/div[1]/span'
    persentase_chat_dibalas = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[3]/div/div[1]/span'

    # Wait for the container to appear
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath1)))
        # Count Child divs under xpath1
        parent = driver.find_element(By.XPATH, xpath1)
        child_divs = parent.find_elements(By.XPATH, "./div")
        total_items = len(child_divs)
        print(f"[INFO] Total Items Found: ", total_items)
        # Loop through and extract values using xpath_loop
        for i in range(1, total_items + 1):
            xpath = xpath_loop.format(loop=i)
            xpath_total_produk = total_produk.format(loop=i)
            xpath_penilaian = penilaian.format(loop=i)
            xpath_persentase_chat_dibalas = persentase_chat_dibalas.format(loop=i)
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                element_total_produk = wait.until(EC.presence_of_element_located((By.XPATH, xpath_total_produk)))
                element_penilaian = wait.until(EC.presence_of_element_located((By.XPATH, xpath_penilaian)))
                element_persentase_chat_dibalas = wait.until(EC.presence_of_element_located((By.XPATH, xpath_persentase_chat_dibalas)))
                print(f"Item {i}: {element.text} (total_produk: {element_total_produk.text}, penilaian: {element_penilaian.text}, persentase chat dibalas: {element_persentase_chat_dibalas.text})")
                # with open("list_toko", "w") as f:
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

def parse_args():
    parser = argparse.ArgumentParser(description="This Is Shopee Store Scraper With Selenium")
    parser.add_argument("--wordlist", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    # with open(args.wordlist, "r") as f:
    #     keyword = f.read()
    #     print(f"{keyword}")
    # sys.exit()
    
    if args.wordlist:
        with open(args.wordlist, "r") as f:
            wordlist = f.readlines()
            for keyword in wordlist:
                scrape_username_toko(keyword)
    else:
        print("Tolong Masukan Wordlist dari toko yang ingin dicari")
# https://shopee.co.id/verify/captcha?anti_bot_tracking_id=VTJGc2RHVmtYMSs2QzZTMHJzSW5La212eHdnak1Yb0o2SS9uWXY5RXoyRCtQT01rUzB3NldCdnB5dUVUSEcwaTFlK3l2bXgrQnNsdEJSVEN1U2NxbXEwWXRPYmNxNUdLSXFnc3cxUWhxQzVtYmZJRm1UeXFQS1FJSGJuU08yWWlLOWllTlpUeGduUUgwRTRlZm1JMU1aWVVRakpabVVyTDhackdweWhsT1UwVFZJWFJyUXVmNTYvL1VxdjVxSzgxRHU2WDdhMUZwdnZZbjZPaDI4bW0vSVBqbWIyL2RMVCs1UFdXdGJ4NHR6UzROKzBuamFhZnN1UkdBR3BrWG1VYTR5ajEvK0pHdllQaVE4TkxXN3Y1UmxkdXIxRTFNTHVKSENmZHZIbmdEcWxBUzNka0JFKzUyWVZ1R0F5VEFpMnZIaWxwTWlTYjgvS1VMUkEyd3hoK2hXNXVkNHZBWDZrRlVyZTNEUmR2WDlxV2VoSjFWdHIzOUZZeGo0OUxpUzRaNDBXd1hNNDJKS2I5TSszZEM0cVB6WWtsNEFkQVdoUkg4VnY4bEFPMHA2disweG9UMERmRS9sa3lYd09XcUdtUklHbkloRFJQY0diUTVPMzUvUFMrdGNTUmpPTFdianY0bmg1akdXQllJbGFZWkJZTnZDSHpib1VKVTFxWXBnZk9uUW0xdko1eldpcjNLZmQ1L1F4K0VwZXAwSTVmck94YzJKZGJrVWtFV1czM2tHVU1tU0dON3ErOXdublA2Ympkc1dPK3VDeU1DcWprUnBjdjd0OXg5QW8vbXVBZHNXNnVidUg5OHFkNlB4aEpUckhqbzFtMUZwY3lvSkNCa0JjQks0ckx0Qjc1MmE1dVVCNlU3THM2dmhVUm9ETFd6eGV3YWMwb05KUTVaSS93dXlSNnJzQ0FpN2lYQW5RakoxU281c3dwcUxzTWN5QkVnVXBlMnFkeGRyd3R5VVBIYXJXV3dPa0VwUEd1YW1wK1h4MC9iNUVsRmJOYWZFbDFwTmpFY0Fxd3BMKzdGeVVyNHlLL0FOTjhDS2lGa1lJd2UyMmpTMDl3UG92N0JteldsOEN6WkFkUXVRK3NDRmV1QzdVUFl0L0JFSUdrYTRjUkdXWGE3ZnhHQmUrY0Jlajd5VWJuZlFwNm5ISTJpc3ZGNDByT09YL2c1NUhUMDhnTXBZemFGS2dOTVZTUzFwdkc1UG9CS0VmWXhJVnZqVmhkYU9zV1NVcXpYUjFTWkZMbng1dlVoL3NnbEJiMm1jaXpsOTNsOUdjTzQ1ZkZyU2lWYXl5aUNkUkNLS2srWUF2RDFScUw1dVRUZ0pXakZHRkFDOVV1V0t5WlREZnpuUHhDbmVndG5IN3FTbW1ZRWRQOUs0RVBaSFI4QU1BSm5IMk5OdFVvNGtxeFFPYVBvdlNnVTI2ODB2VmZMOFphU2tSYXRxNEVmcHRjMGRuZ0Q4K1RydE5pZHNvZWlwWU9aUDJqaS9rSWFDd3EybVMwWGdzRTRJWG8zaWNGM1NDYm5GZmVrZ1loTHVsaExkK25haEVVTXFCallmMjdWMnkvaEUxTEF3bWhWREkzeVB1dUlGVjA0NURHMEFDYkJtUGhWQUFhQnU3Zg&app_key=Cart.PC&client_id=1&next=https%3A%2F%2Fshopee.co.id%2Fverify%2Ftraffic&redirect_type=2&scene=crawler_item&should_replace_history=true