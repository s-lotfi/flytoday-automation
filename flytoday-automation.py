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

def close_popups(timeout=3):

    end_time = time.time() + timeout
    while time.time() < end_time:
        
        try:
            iframe = driver.find_element(By.ID, "webpush-onsite")
            driver.execute_script("arguments[0].style.display='none';", iframe)  # iframe را مخفی کن
            driver.switch_to.default_content()
        except:
            driver.switch_to.default_content()
            pass

        xpaths = [
            "//button[contains(text(),'متوجه شدم')]",
            "//button[contains(text(),'باشه')]",
            "//button[contains(text(),'بعدی')]",
            "//button[contains(text(),'بستن')]",
            "//button[contains(@class,'close')]",
            "//div[contains(@class,'close')]"
        ]
        for xp in xpaths:
            try:
                btns = driver.find_elements(By.XPATH, xp)
                for btn in btns:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.2)
            except:
                pass

def select_city(button_css, cities, exclude=None):
    close_popups()  
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css)))
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(0.5)

    city = random.choice(cities)
    while city == exclude:
        city = random.choice(cities)

    options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='option']")))
    for option in options:
        if city in option.text:
            driver.execute_script("arguments[0].click();", option)
            break
    time.sleep(0.5)
    return city

def select_random_day():
    close_popups()
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="start-date-field"]')))
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(0.5)

    while True:
        close_popups()
        days = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-test^='calendarDay-']:not([disabled])"))
        )
        if days:
            day = random.choice(days)
            driver.execute_script("arguments[0].click();", day)
            confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="confirmDate"]')))
            driver.execute_script("arguments[0].click();", confirm_btn)
            time.sleep(0.5)
            break
        else:
            next_month = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='calendar-next-month']")))
            driver.execute_script("arguments[0].click();", next_month)
            time.sleep(0.5)

try:
    driver.get("https://www.flytoday.ir")
    time.sleep(1)

    cities = ["تهران", "مشهد", "شیراز", "کیش", "اصفهان"]

    origin = select_city('button[data-test="flight-origin"]', cities)
    destination = select_city('button[data-test="flight-destination"]', cities, exclude=origin)

    select_random_day()

    close_popups()
    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="flightSearchBtn"]')))
    driver.execute_script("arguments[0].click();", search_btn)

    time.sleep(3)
    close_popups()

    try:
        tickets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.itinerary_wrapper__j2RSA")))
        print(f"✅🛫 Tickets available — Total: {len(tickets)} — From: {origin}, To: {destination}")
    except:
        print(f"❌🛬 Tickets not available — From: {origin}, To: {destination}")
    time.sleep(2)

finally:
    driver.quit()
