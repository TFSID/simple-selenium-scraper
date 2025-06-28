from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import sys
import argparse
import os

# Set your Chrome user data path (adjust this!)
user_data_dir = r"C:\Users\Akasata\AppData\Local\BraveSoftware\Brave-Browser\User Data"
profile_dir = "Profile 3"  # or "Profile 1", etc.

def scrape_username_toko(keyword):
    keyword = keyword.strip()  # Remove whitespace/newlines
    print(f"[INFO] Searching for keyword: '{keyword}'")
    
    # Configure Chrome options for undetected-chromedriver
    chrome_options = uc.ChromeOptions()
    
    # Profile settings
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    
    # Anti-detection settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # User agent to appear more natural
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # Initialize undetected Chrome driver
        driver = uc.Chrome(options=chrome_options, version_main=None)
        wait = WebDriverWait(driver, 15)
        
        # Navigate to search page
        search_url = f"https://shopee.co.id/search_user?keyword={keyword}"
        print(f"[INFO] Navigating to: {search_url}")
        driver.get(search_url)
        
        # Wait a bit for page to load
        time.sleep(3)
        
        # Check if captcha or verification page appears
        if "verify" in driver.current_url or "captcha" in driver.current_url:
            print("[WARN] Captcha or verification page detected. Please solve it manually.")
            input("After solving captcha, press Enter to continue...")
        
        # Define XPath patterns
        xpath_container = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]'
        xpath_shop_name = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/a/div[2]'
        xpath_total_products = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[1]/div/div[1]/span'
        xpath_rating = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[2]/div/div[1]/span'
        xpath_chat_response = '//*[@id="main"]/div/div[2]/div/div/div/div/div/div[2]/div[{loop}]/div[2]/div[3]/div/div[1]/span'
        
        # Wait for the container to appear
        print("[INFO] Waiting for search results to load...")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
            
            # Count child divs under container
            parent = driver.find_element(By.XPATH, xpath_container)
            child_divs = parent.find_elements(By.XPATH, "./div")
            total_items = len(child_divs)
            
            if total_items == 0:
                print("[WARN] No search results found")
                return
                
            print(f"[INFO] Total Items Found: {total_items}")
            
            # Prepare results list
            results = []
            
            # Loop through and extract values
            for i in range(1, total_items + 1):
                try:
                    # Build XPaths for current item
                    current_shop_xpath = xpath_shop_name.format(loop=i)
                    current_products_xpath = xpath_total_products.format(loop=i)
                    current_rating_xpath = xpath_rating.format(loop=i)
                    current_chat_xpath = xpath_chat_response.format(loop=i)
                    
                    # Extract shop name (required)
                    shop_element = wait.until(EC.presence_of_element_located((By.XPATH, current_shop_xpath)))
                    shop_name = shop_element.text.strip()
                    
                    # Extract optional elements with fallback
                    try:
                        products_element = driver.find_element(By.XPATH, current_products_xpath)
                        total_products = products_element.text.strip()
                    except:
                        total_products = "N/A"
                    
                    try:
                        rating_element = driver.find_element(By.XPATH, current_rating_xpath)
                        rating = rating_element.text.strip()
                    except:
                        rating = "N/A"
                    
                    try:
                        chat_element = driver.find_element(By.XPATH, current_chat_xpath)
                        chat_response = chat_element.text.strip()
                    except:
                        chat_response = "N/A"
                    
                    # Store result
                    result = {
                        'shop_name': shop_name,
                        'total_products': total_products,
                        'rating': rating,
                        'chat_response': chat_response
                    }
                    results.append(result)
                    
                    print(f"Item {i}: {shop_name} (Products: {total_products}, Rating: {rating}, Chat Response: {chat_response})")
                    
                except Exception as e:
                    print(f"[WARN] Element {i} not found or failed to load. Error: {e}")
                    continue
            
            # Save results to file
            if results:
                filename = f"shopee_stores_{keyword.replace(' ', '_')}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Search Results for: {keyword}\n")
                    f.write("=" * 50 + "\n\n")
                    for idx, result in enumerate(results, 1):
                        f.write(f"{idx}. Shop: {result['shop_name']}\n")
                        f.write(f"   Products: {result['total_products']}\n")
                        f.write(f"   Rating: {result['rating']}\n")
                        f.write(f"   Chat Response: {result['chat_response']}\n\n")
                print(f"[INFO] Results saved to: {filename}")
            
        except Exception as e:
            print(f"[ERROR] No results found or page structure changed: {e}")
            # Take screenshot for debugging
            try:
                driver.save_screenshot(f"debug_screenshot_{keyword.replace(' ', '_')}.png")
                print(f"[DEBUG] Screenshot saved for debugging")
            except:
                pass
                
    except Exception as e:
        print(f"[ERROR] Failed to initialize driver or load page: {e}")
    
    finally:
        if driver:
            # Wait before closing for review (optional)
            if len(sys.argv) > 1 and "--debug" in sys.argv:
                input("Press Enter to exit and close browser...")
            driver.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Shopee Store Scraper with Selenium and Undetected ChromeDriver")
    parser.add_argument("--wordlist", type=str, help="Path to wordlist file containing search keywords")
    parser.add_argument("--keyword", type=str, help="Single keyword to search")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with manual browser close")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    # Check if profile directory exists
    full_profile_path = os.path.join(user_data_dir, profile_dir)
    if not os.path.exists(full_profile_path):
        print(f"[ERROR] Profile directory does not exist: {full_profile_path}")
        print("Please check your user_data_dir and profile_dir settings.")
        sys.exit(1)
    
    if args.wordlist:
        if not os.path.exists(args.wordlist):
            print(f"[ERROR] Wordlist file not found: {args.wordlist}")
            sys.exit(1)
            
        print(f"[INFO] Loading wordlist from: {args.wordlist}")
        with open(args.wordlist, "r", encoding="utf-8") as f:
            wordlist = f.readlines()
            
        for keyword in wordlist:
            keyword = keyword.strip()
            if keyword:  # Skip empty lines
                print(f"\n[INFO] Processing keyword: {keyword}")
                scrape_username_toko(keyword)
                time.sleep(2)  # Delay between searches to avoid rate limiting
                
    elif args.keyword:
        scrape_username_toko(args.keyword)
    else:
        print("[ERROR] Please provide either --wordlist or --keyword parameter")
        print("Usage examples:")
        print("  python script.py --keyword 'electronics'")
        print("  python script.py --wordlist keywords.txt")
        print("  python script.py --wordlist keywords.txt --debug")

if __name__ == "__main__":
    main()