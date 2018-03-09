from trendyolClass import TrendyolTests

# Bir instance alalım, parametre olarak chrome veya firefox girilebilir.
trendyol = TrendyolTests("chrome")
trendyol.loginStorefront() #Login ol

trendyolCategories = [
"/",
"/Butik/Liste/Kadin",
"/Butik/Liste/Erkek",
"/Butik/Liste/cocuk",
"/Butik/Liste/Spor--Giyim",
"/Butik/Liste/Ayakkabi--canta",
"/Butik/Liste/Saat--Aksesuar",
"/Butik/Liste/Kozmetik",
"/Butik/Liste/Ev--Yasam",
"/Butik/Liste/Hizli--Teslimat"
]
# Her bir kategoriye bağlanarak butik resimlerini kontrol edelim.
for category in trendyolCategories:
    trendyol.getUrl(category) # anasayfaya git
    trendyol.checkBoutiqueImages() # Girdiğin kategorideki butik resimlerinde problem var mı kontrol et.

# Belirtilen butik içerisindeki ürün resimleri status_code = 200 mü?
trendyol.checkProductImageInBoutique("/Parfumde-Dev-indirim/ButikDetay/179213/Kozmetik")

# Bir ürünün detayına gir, sepete at sonra kontrol et o ürün adı sepette mi?
trendyol.getUrl("/lancome/lancome-miracle-edp-30-ml-body-lotion-50-ml-shower-gel-50-ml-kadin-parfum-seti-p-1164468")
urunAdi = trendyol.getProductName()
trendyol.addBasket()
trendyol.checkProductInTheBasket(urunAdi)

trendyol.close_connection() # tarayıcıyı kapat.
