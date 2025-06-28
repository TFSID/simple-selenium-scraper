import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Set your Chrome user data path (adjust this!)
user_data_dir = r"C:\\Users\\Akasata\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Profile 1"  # or "Profile 1", etc.

def create_driver(profile_dir="chrome_profile"):
    profile_path = os.path.abspath(profile_dir)

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")

    print(f"[INFO] Starting Chrome with profile at: {profile_dir}")
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver

def repl(driver):
    print("\n💡 Enter commands to control the browser:")
    print("   - go https://example.com")
    print("   - click .btn-login")
    print("   - fill #username myname")
    print("   - screenshot result.png")
    print("   - exit\n")

    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue

            if cmd == "exit":
                print("[INFO] Exiting browser...")
                driver.quit()
                break

            elif cmd.startswith("go "):
                url = cmd[3:].strip()
                if not url.startswith("http"):
                    url = "https://" + url
                print(f"[INFO] Navigating to: {url}")
                driver.get(url)

            elif cmd.startswith("click "):
                selector = cmd[6:].strip()
                elem = driver.find_element(By.CSS_SELECTOR, selector)
                elem.click()
                print(f"[INFO] Clicked: {selector}")

            elif cmd.startswith("fill "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    print("[ERROR] Usage: fill <selector> <text>")
                    continue
                selector, text = parts[1], parts[2]
                elem = driver.find_element(By.CSS_SELECTOR, selector)
                elem.clear()
                elem.send_keys(text)
                print(f"[INFO] Filled: {selector} with '{text}'")

            elif cmd.startswith("screenshot "):
                filename = cmd.split(" ", 1)[1]
                driver.save_screenshot(filename)
                print(f"[INFO] Screenshot saved to {filename}")

            else:
                print("[ERROR] Unknown command. Type 'exit' to quit.")

        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    print("🌐 Selenium CLI Interactive Browser")
    url = input("🔗 Enter the URL to visit (e.g., https://www.google.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    driver = create_driver()
    driver.get(url)
    time.sleep(2)  # Wait for page load

    repl(driver)

if __name__ == "__main__":
    main()
