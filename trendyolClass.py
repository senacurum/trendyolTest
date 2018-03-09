from config import *
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TrendyolTests():
    """Trendyol test senaryoları için gerekli olan methodları barındıran sınıf."""
    def __init__(self,driver):
        self.base_url = "https://www.trendyol.com"
        self.username = trendyol_username
        self.password = trendyol_password
        if driver == "chrome":
            self.browser = webdriver.Chrome(executable_path=chrome_driver_path)
        else:
            self.browser = webdriver.Firefox(executable_path=firefox_driver_path)
        self.browser.maximize_window()

    def getUrl(self,url):
        self.browser.get(self.base_url + url)
        self.waitForLoadText()

    def waitForLoadText(self,inputLinkText = "Kullanım Koşulları"):
        delay = 4 #saniye
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.LINK_TEXT, inputLinkText)))
            # Sayfa {delay} saniye içinde yüklendi.
        except TimeoutException:
            logging.error("{} sayfası {} saniyeden geç açıldı".format(self.browser.current_url,delay))
            pass

    def loginStorefront(self):
        self.getUrl("/login")
        self.browser.find_element_by_id("fEmailx").send_keys(self.username)
        self.browser.find_element_by_id("LoginModel_Password").send_keys(self.password)
        self.browser.find_element_by_id("loginSubmitButton").click()

    # Gönderilen imageUrl değerine istek atarak başarıyla ulaşıp ulaşamadığını kontrol eder.
    def isImageStatusOk(self,imageUrl):
        try:
            r = requests.get(imageUrl)
            if not r.status_code // 100 == 2:
                logging.error("{} için beklenmedik response {}".format(imageUrl,r))
                return False
            else:
                return True
        except requests.exceptions.RequestException as e:
            # Ciddi bir sorun var, SSLError veya InvalidURL
            logging.error("{} için hata: {}".format(imageUrl,e))
            return False

    def checkBoutiqueImages(self):
        images = self.browser.find_elements_by_css_selector("img.bigBoutiqueImage")
        for image in images:
            if not self.isImageStatusOk(image.get_attribute("data-original")):
                logging.error("{} butiğindeki {} görseline ulaşılamadı.".format(image.get_attribute("title"),image.get_attribute("data-original")))
        logging.info("{} kategorisindeki butik resimleri kontrol edildi.".format(self.browser.current_url))

    def checkProductImageInBoutique(self,category):
        self.category = self.base_url + category
        try:
            r = requests.get(self.category)
        except Exception:
            logging.error(self.category," kategorisine bağlanılamadı.")

        source = BeautifulSoup(r.content,"lxml")
        images = source.findAll("product-zoom-gallery")
        for image in images:
            if not self.isImageStatusOk(image.get("photo")):
                logging.error("{} butiğindeki {} görseline ulaşılamadı.".format(self.category,image.get("photo")))
        logging.info("{} butiğindeki ürün resimleri kontrol edildi.".format(self.category))

    # Ürünü sepete atar.
    def addBasket(self):
        self.browser.find_element_by_xpath('//*[@id="addToBasketButton"]/span[1]').click()

    # Ürünün adını döndürür.
    def getProductName(self):
        return self.browser.find_element_by_xpath('/html/head/meta[21]').get_attribute("content")

    # Parametre olarak gönderilen ürün adı sepet içerisinde mi kontol eder.
    def checkProductInTheBasket(self,checkProductName):
        self.getUrl("/c/sepetim#/basket")
        self.waitForLoadText("Alışverişe Devam Et")
        productNameInTheBasket = self.browser.find_element_by_xpath('//*[@id="basketContent"]/div[2]/div/ul/li/div[2]/div[1]/a/span[2]').text
        if productNameInTheBasket != checkProductName:
            logging.error("{} ürünü sepette değil.".format(checkProductName))
        else:
            logging.info("{} ürünü başarıyla sepete atılmış.".format(checkProductName))

    def close_connection(self):
        self.browser.close()
