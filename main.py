from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
import time


def image_to_text(api_key, base64_image):
    url = 'https://api.ocr.space/parse/image'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'apikey': api_key,
        'base64Image': base64_image
    }
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result.get('ParsedResults', [{}])[0].get('ParsedText', '').strip()



driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get("https://sdms.udiseplus.gov.in/p1/v1/login?state-id=109")

driver.find_element(By.ID, "username-field").send_keys("username")
driver.find_element(By.ID, "password-field").send_keys("password")

base64_image = driver.execute_script("""
    var img = document.getElementById('captchaImage');
    if (img) {
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        context.drawImage(img, 0, 0);
        return canvas.toDataURL('image/png');
    }
    return null;""")
api_key = 'K81986050988957'
captcha = image_to_text(api_key, base64_image)

driver.find_element(By.ID, "captcha").send_keys(captcha)
driver.find_element(By.ID, "submit-btn").click()

if "error=Invalid%20Captcha" in driver.current_url:
    print("wrong Captcha")

time.sleep(2)

driver.find_element(By.XPATH, "//li[@class='shadow-lg orangeBack']").click()

driver.get("https://sdms.udiseplus.gov.in/g1/#/school/2185508/listAllStudentCy")


pen=["21345212399"]
for num in pen:
    
    search = driver.find_element(By.ID, "mat-input-1")
    search.clear()
    search.send_keys(num)

    
    driver.find_element(By.XPATH,
                        "//*[@id='page-content-wrapper']/main/div/div/div/app-listallstudent-cy/div[2]/div/div[2]/div[2]/table/tbody/tr/td[2]/p[1]/span").click()

    dob = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='dob']").get_attribute("value")
    addres = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='address']").get_attribute("value")

    print(dob)
    print(addres)
    print()
