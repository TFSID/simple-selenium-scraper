import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Set your Chrome user data path (adjust this!)
user_data_dir = r"C:\\Users\\Akasata\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Profile 1"  # or "Profile 1", etc.


def create_driver(profile_dir="chrome_profile"):
    # Ensure absolute path for profile
    # profile_path = os.path.abspath(profile_dir)

    # Create Chrome options
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")

    # Optional: uncomment for headless mode
    # options.add_argument("--headless=new")

    # Create WebDriver
    print(f"[INFO] Starting Chrome with profile at: {user_data_dir}")
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver

def main():
    print("🌐 Selenium CLI Interactive Browser")
    url = input("🔗 Enter the URL to visit (e.g., https://www.google.com): ").strip()

    if not url.startswith("http"):
        url = "https://" + url  # Add scheme if missing

    driver = create_driver()

    print(f"[INFO] Navigating to: {url}")
    try:
        driver.get(url)
        print("[INFO] Browser is open. Press CTRL+C to close manually.")
    except Exception as e:
        print(f"[ERROR] Failed to open the URL: {e}")
        driver.quit()

if __name__ == "__main__":
    main()
