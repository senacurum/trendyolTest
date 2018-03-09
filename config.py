import logging

# TrendyolConfig
trendyol_username = "login@mail.com"
trendyol_password = 123456

"""
DriverConfig
Chrome Driver İndir: https://chromedriver.storage.googleapis.com/index.html?path=2.35/
Firefox Driver İndir: https://github.com/mozilla/geckodriver/releases
"""
chrome_driver_path = "/home/sinan/Downloads/selenium/chromedriver"
firefox_driver_path = "/home/sinan/Downloads/selenium/geckodriver"

# logConfig
logging.basicConfig(
filename="testResults.log",
level=logging.INFO,
format="%(asctime)s:%(levelname)s:%(message)s")
