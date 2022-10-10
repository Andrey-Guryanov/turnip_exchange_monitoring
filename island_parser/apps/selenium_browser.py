from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import LOG_PATH

Path(LOG_PATH).mkdir(parents=True, exist_ok=True)


def _create_driver(driver_path, user_agent):
    driver_option = Options()
    driver_option.headless = True
    driver_option.set_preference('dom.webdriver.enabled', False)
    driver_option.set_preference('general.useragent.override', user_agent)
    driver_location = str(driver_path)
    driver = webdriver.Firefox(executable_path=driver_location,
                               service_log_path=str(LOG_PATH / 'geckodriver.log'),
                               options=driver_option)
    driver.set_page_load_timeout(60)
    driver.set_window_size(800, 600)
    return driver


def get_content(user_agent, url, element_wait_xpath, driver_path):
    browser_driver = _create_driver(driver_path, user_agent)
    try:
        browser_driver.get(url)
        delay_wait = 10
        WebDriverWait(browser_driver, delay_wait).until(
            EC.visibility_of_element_located((By.XPATH, element_wait_xpath)))
    except TimeoutException:
        print("TimeoutException")
        return ''
    finally:
        all_html_content = browser_driver.page_source
        browser_driver.save_screenshot(f'test.png')
        browser_driver.close()
        return all_html_content
