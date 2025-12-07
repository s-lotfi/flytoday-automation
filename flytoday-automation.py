import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

def close_popups(timeout=5):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            driver.switch_to.frame(driver.find_element(By.ID, "webpush-onsite"))
            driver.find_element(By.ID, "deny").click()
            driver.switch_to.default_content()
        except:
            driver.switch_to.default_content()
        for xpath in ["//button[contains(text(),'متوجه شدم')]",
                      "//button[text()='بعدی']",
                      "//button[text()='×' or contains(@class,'close')]"]:
            try:
                for btn in driver.find_elements(By.XPATH, xpath):
                    btn.click()
                    time.sleep(0.2)
            except:
                pass

def select_city(button_css, cities, exclude=None):
    close_popups()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css))).click()
    time.sleep(0.5)
    city = random.choice(cities)
    while city == exclude:
        city = random.choice(cities)
    for option in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='option']"))):
        if city in option.text:
            option.click()
            break
    time.sleep(0.5)
    return city

def select_random_day():
    close_popups()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="start-date-field"]'))).click()
    time.sleep(0.5)
    while True:
        close_popups()
        days = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button[data-test^='calendarDay-']:not([disabled])")
        ))
        if days:
            driver.execute_script("arguments[0].click();", random.choice(days))
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="confirmDate"]'))).click()
            time.sleep(0.5)
            break
        else:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='calendar-next-month']"))).click()
            time.sleep(0.5)

try:
    driver.get("https://www.flytoday.ir")
    time.sleep(1)
    cities = ["تهران", "مشهد", "شیراز", "کیش", "اصفهان"]
    origin = select_city('button[data-test="flight-origin"]', cities)
    destination = select_city('button[data-test="flight-destination"]', cities, exclude=origin)
    select_random_day()
    close_popups()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="flightSearchBtn"]'))).click()
    time.sleep(3)
    close_popups()
    try:
        tickets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.itinerary_wrapper__j2RSA")))
        if tickets:
            print(f"✅🛫 Tickets available — Total: {len(tickets)} — From: {origin}, To: {destination}")
        else:
            print(f"❌🛬 Tickets not available — From: {origin}, To: {destination}")
    except:
        print("⚠️🕒 Search results not found or page did not load correctly")
    time.sleep(3)
finally:
    driver.quit()
