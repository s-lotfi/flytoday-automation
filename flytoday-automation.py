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

def close_all_popups_loop():

    end_time = time.time() + 5
    while time.time() < end_time:

        try:
            iframe = driver.find_element(By.ID, "webpush-onsite")
            driver.switch_to.frame(iframe)
            deny_btn = driver.find_element(By.ID, "deny")
            deny_btn.click()
            driver.switch_to.default_content()
            time.sleep(0.2)
        except:
            driver.switch_to.default_content()
            pass

        try:
            buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'متوجه شدم')]")
            for btn in buttons:
                try:
                    btn.click()
                    time.sleep(0.2)
                except:
                    continue
        except:
            pass

        try:
            next_btn = driver.find_element(By.XPATH, "//button[text()='بعدی']")
            next_btn.click()
            time.sleep(0.2)
        except:
            pass

        try:
            close_buttons = driver.find_elements(By.XPATH, "//button[text()='×' or contains(@class,'close')]")
            for btn in close_buttons:
                try:
                    btn.click()
                    time.sleep(0.2)
                except:
                    continue
        except:
            pass

try:
    driver.get("https://www.flytoday.ir")
    time.sleep(2)

    cities = ["تهران", "مشهد", "شیراز", "کیش", "اصفهان"]

    close_all_popups_loop()
    origin_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="flight-origin"]'))
    )
    origin_button.click()
    time.sleep(1)

    origin_city = random.choice(cities)
    origin_options = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='option']"))
    )
    for option in origin_options:
        if origin_city in option.text:
            option.click()
            break
    time.sleep(1)

    close_all_popups_loop()
    destination_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="flight-destination"]'))
    )
    destination_button.click()
    time.sleep(1)

    destination_city = origin_city
    while destination_city == origin_city:
        destination_city = random.choice(cities)

    destination_options = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='option']"))
    )
    for option in destination_options:
        if destination_city in option.text:
            option.click()
            break
    time.sleep(1)

    close_all_popups_loop()
    start_date_field = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="start-date-field"]'))
    )
    start_date_field.click()
    time.sleep(2)

    while True:
        close_all_popups_loop()
        active_days = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button[data-test^='calendarDay-']:not([disabled])")
            )
        )
        if active_days:
            day_to_click = random.choice(active_days)
            driver.execute_script("arguments[0].click();", day_to_click)
            time.sleep(1)

            confirm_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="confirmDate"]'))
            )
            confirm_button.click()
            time.sleep(1)
            break
        else:
            next_month = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='calendar-next-month']"))
            )
            next_month.click()
            time.sleep(1)

    close_all_popups_loop()
    search_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="flightSearchBtn"]'))
    )
    search_button.click()
    time.sleep(5)
    close_all_popups_loop()

    try:
        tickets = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.itinerary_wrapper__j2RSA"))
        )
        if tickets:
            print(f"✅🛫 Tickets available — Total: {len(tickets)} — From: {origin_city}, To: {destination_city}")
        else:
            print(f"❌🛬 Tickets not available — From: {origin_city}, To: {destination_city}")
    except:
        print("⚠️🕒 Search results not found or page did not load correctly")

    time.sleep(5)

finally:
    driver.quit()
