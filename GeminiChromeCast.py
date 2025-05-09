from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from appium.options.common.base import AppiumOptions

API_KEY = os.environ["API_KEY"]
api_token = API_KEY

APPIUM = f'https://dev-us-sny-9.headspin.io:7028/v0/{api_token}/wd/hub'

CAPS = {
    "deviceName": "Chromecast",
    "udid": "17081HFDD2699Y",
    "automationName": "uiautomator2",
    "platformName": "android",
    "headspin:capture.video": "True",
    # "headspin:testName": "David-Test",
    "appPackage": "com.tubitv",
    "appActivity": ".activities.MainActivity",
    "headspin:newCommandTimeout": 180,
    # "headspin:appiumVersion": "2.0.0",
}
options = AppiumOptions()
options.load_capabilities(CAPS)
driver = webdriver.Remote(
    command_executor=APPIUM,
    options=options
)
try:
    #driver.get('https://the-internet.herokuapp.com')
    #Tubi
    #//android.widget.TextView[@resource-id="intro"]
  #  wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.LinearLayout[@resource-id="com.tubitv:id/action_bar_root"]')))
    time.sleep(30)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(66)
    

    time.sleep(10)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(66)

    time.sleep(5)
    driver.press_keycode(21)
    time.sleep(2)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(20)
    time.sleep(2)
    driver.press_keycode(66)
    time.sleep(2)
    driver.press_keycode(66)

    time.sleep(90)
    with open("session_info.txt", "w") as file:
        file.write(driver.session_id)


finally:
    driver.quit()
