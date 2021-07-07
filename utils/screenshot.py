from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def screenshot(url):
    try:
        options = Options()
        options.headless = True
        options.add_argument('ignore-certificate-errors')
        path = 'images/'+url.split("/")[2]+'.png'
        driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
        driver.set_page_load_timeout(3)
        driver.get(url)
        driver.get_screenshot_as_file(path)
        driver.quit()
    except:
        driver.quit()
        print(f"cannot get {url}")