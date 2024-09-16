from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
import time

# Initialize Edge WebDriver
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

# Open the login page
driver.get("https://sdms.udiseplus.gov.in/p1/v1/login?state-id=109")

# Enter username and password
driver.find_element(By.ID, "username-field").send_keys("user")
driver.find_element(By.ID, "password-field").send_keys("pass")

input("Enter: ")

# Click the submit button to log in
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "submit-btn"))).click()
# Wait for and click the 'Go to 2024-25' button
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Go to 2024-25')]"))).click()
# Close any overlay or pop-up
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'btn-danger') and text()='Close']"))).click()

# List of student pens (IDs)
pens=[]
# Loop through each student ID and extract details

def getData(pen):
    driver.get("https://sdms.udiseplus.gov.in/g1/#/school/2185508/listAllStudentCy")

    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, "preloader")))

    search = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id^='mat-input-']")))
    search.clear()
    search.send_keys(pen)
    search.send_keys(Keys.RETURN)

    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='page-content-wrapper']/main/div/div/div/app-listallstudent-cy/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/p[1]/span"))).click()
        
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'cdk-step-label-') and contains(., 'Profile Preview')]"))).click()
    #time.sleep(1)

    dob = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="print-section"]/div[2]/table/tr[1]/td/div/div/div[2]/div/table/tr[3]/td'))).text
    address = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="print-section"]/div[2]/table/tr[1]/td/div/div/div[2]/div/table/tr[10]/td'))).text
    admission_number = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="print-section"]/div[2]/table/tr[2]/td/div/div/div[2]/div/table/tr[1]/td'))).text
    height = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="print-section"]/div[2]/table/tr[3]/td/div/div[2]/div[2]/div/table/tr[11]/td'))).text
    weight = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="print-section"]/div[2]/table/tr[3]/td/div/div[2]/div[2]/div/table/tr[12]/td'))).text
    return dob, address, admission_number, height, weight

dobs, addresses, adm_nums, weights, heights = [], [], [], [], []
for pen in pens:
    while True:  # Loop until valid data is obtained
        try:
            dob, address, admission_number, height, weight = getData(pen)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            continue
        print(f"dob: '{dob}'")
        print(f"address: '{address}'")
        print(f"admission_number: '{admission_number}'")
        print(f"height: '{height}'")
        print(f"weight: '{weight}'")
        
        if admission_number == 'NA' and dob == '' and address == 'NA' and height == 'NA' and weight == 'NA':
            print(f"{pens.index(pen)}, {pen} has missind data, trying again...")

        else:
            break

    # Once valid data is found, append to respective lists
    dobs.append(dob)
    addresses.append(address)
    adm_nums.append(admission_number)
    weights.append(weight)
    heights.append(height)
