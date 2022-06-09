from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":

    # Paths for local testing to be adjusted for the following variables:
    filePath = "C:\L7\code\census_2009b" 
    executable_path = "C:\L7\code\chromedriver.exe"

    driver = webdriver.Chrome(executable_path)
    driver.implicitly_wait(0.5)
    driver.maximize_window()

    # Load web application
    driver.get("http://localhost:5000")
    time.sleep(5)
    
    # Upload the sample file `census_2009b``
    driver.find_element_by_id("uploadfile").send_keys(filePath)
    time.sleep(2.5)

    # Click submit button and see first graph that corresponds to Benford's assertion  
    driver.find_element_by_id("submitbutton").click()
    time.sleep(5)

    # TODO: Try the following graph, if any othercolumns exist  
    # driver.find_element_by_id("selectedColumn").click()
    # time.sleep(5)

    driver.close()