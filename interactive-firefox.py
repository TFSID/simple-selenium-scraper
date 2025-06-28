import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time

# Set your Firefox profile path (adjust this!)
# On Windows: C:\\Users\\YourUsername\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\
# On macOS: ~/Library/Application Support/Firefox/Profiles/
# On Linux: ~/.mozilla/firefox/
profile_path = r"C:\\Users\\Akasata\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\your-profile-name.default-release"

def create_driver(profile_path=None):
    options = Options()
    
    # Set Firefox profile if provided
    if profile_path and os.path.exists(profile_path):
        options.add_argument(f"-profile")
        options.add_argument(profile_path)
        print(f"[INFO] Using Firefox profile at: {profile_path}")
    else:
        print("[INFO] Using default Firefox profile")
    
    # Firefox-specific options
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    
    # Additional preferences
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    
    print(f"[INFO] Starting Firefox...")
    driver = webdriver.Firefox(service=Service(), options=options)
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
    print("🦊 Selenium CLI Interactive Browser (Firefox)")
    url = input("🔗 Enter the URL to visit (e.g., https://www.google.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    driver = create_driver(profile_path)
    driver.get(url)
    time.sleep(2)  # Wait for page load

    repl(driver)

if __name__ == "__main__":
    main()