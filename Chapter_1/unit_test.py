from main import calculate_sum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def test_user_interface():
    # Path to chromedriver. Ensure this is correct for your environment
    driver_path = r'----------\chromedriver.exe'

	 # Set up options
    options = Options()
    options.add_argument('--headless')  # To not open a real chrome window

 # Use Service to specify the driver path
    service = Service(driver_path)
    
 # Initialize the driver with options and driver path from WebDriverManager
    with webdriver.Chrome(service=service, options=options) as driver:
        url = 'http://127.0.0.1:8501'
        driver.get(url)
        
# Wait for page elements to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            )
            html = driver.page_source
        except Exception as e:
            print(f'Error while waiting for page: {e}')
            html = driver.page_source

    # Perform assertions to check page content
    assert 'Add numbers' in html
    assert 'First Number' in html
    assert 'Second Number' in html

def test_logic():
    assert calculate_sum(1, 1) == 2
    assert calculate_sum(1, -1) == 0
    assert calculate_sum(1, 9) == 10

if __name__ == '__main__':
    test_logic()
    test_user_interface()
