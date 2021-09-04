from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def screenshot(url):
    try:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        path = 'images/'+url.split("/")[2]+'.png'
        driver.set_page_load_timeout(3)
        driver.get(url)
        driver.get_screenshot_as_file(path)
        driver.quit()
    except:
        print(f"cannot get {url}")
