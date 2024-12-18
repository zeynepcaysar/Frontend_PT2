import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_emploi_navigation(driver):
    driver.get("http://127.0.0.1:5000/")
    print("Opened Homepage")

    voir_plus_button_emploi = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-cube .button"))
    )
    voir_plus_button_emploi.click()
    print("Clicked the Voir Plus button in the Emploi Cube")

    WebDriverWait(driver, 10).until(EC.url_contains("/jobs"))
    print("Navigated to: " + driver.current_url)

    # Additional check for an element specific to the Emploi page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".job-cube .button"))
        )
        print("Confirmed Emploi page loaded successfully")
    except:
        driver.save_screenshot('emploi_page_error.png')
        print("Emploi page did not load as expected. Screenshot taken.")

def test_search_navigation(driver):
    driver.get("http://127.0.0.1:5000/")
    print("Opened Homepage")

    voir_plus_button_search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-cube .button"))
    )
    voir_plus_button_search.click()
    print("Clicked the Voir Plus button in the Search Cube")

    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    print("Navigated to: " + driver.current_url)

    # Additional check for an element specific to the Search page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-cube .button"))
        )
        print("Confirmed Search page loaded successfully")
    except:
        driver.save_screenshot('search_page_error.png')
        print("Search page did not load as expected. Screenshot taken.")


def test_keyword_search(driver):
    driver.get("http://127.0.0.1:5000/")
    print("Opened Homepage")

    # Enter a keyword in the search bar
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#search-bar input[type='text']"))
    )
    search_input.send_keys("keyword")

    # Submit the form (assuming there's a submit button, you may need to locate it)
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-bar input[type='submit']"))
    )
    submit_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    print("Navigated to: " + driver.current_url)

    # Additional checks for elements specific to the Search page
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-cube .button"))
        )
        print("Confirmed Search page loaded successfully")
    except Exception as e:
        driver.save_screenshot('search_page_error.png')
        print("Search page did not load as expected. Screenshot taken.")
        raise AssertionError("Search page did not load correctly") from e



if __name__ == "__main__":
    chromedriver_path = '/Users/zeynepcaysar/Downloads/chromedriver_win32'  # Update this path
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=chrome_options)
    try:
        test_emploi_navigation(driver)
        test_search_navigation(driver)
        test_keyword_search(driver)
    finally:
        driver.quit()
