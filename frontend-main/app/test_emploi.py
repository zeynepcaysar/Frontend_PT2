import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_keyword_search_emploi(driver):
    driver.get("http://127.0.0.1:5000/jobs")  # Assuming this URL leads to the "Emploi" page
    print("Opened Emploi Page")

    # Enter a keyword in the search bar
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#emploi-search input[type='text']"))
    )
    search_input.send_keys("keyword")
    # Submit the form (assuming there's a submit button, you may need to locate it)
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#emploi-search input[type='submit']"))
    )
    submit_button.click()

    # Wait for the search results to load (you may need to adjust this wait condition)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results"))
    )

    # Get and print the search results
    search_results = driver.find_elements(By.CSS_SELECTOR, ".search-results .result")
    for result in search_results:
        print(result.text)



if __name__ == "__main__":
    chromedriver_path = '/Users/zeynepcaysar/Downloads/chromedriver_win32'  # Update this path
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=chrome_options)
    try:
        test_keyword_search_emploi(driver)
    finally:
        driver.quit()