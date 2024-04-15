from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService





def scrape_skyscanner(origin, destination, trip_duration, start_date, end_date, proxy):

    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')    
    # Inizializza il WebDriver per Chrome
    print("proxy: " + proxy)

    options = Options()
    options.add_argument('--proxy-server={}'.format(proxy))

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    # Costruisci l'URL per la ricerca su Skyscanner

    #driver.get("https://www.whatismyip.com/proxy-check/?iref=home")

    while start_date + timedelta(days=5) <= end_date:

        trip_end_date = start_date + timedelta(days=trip_duration - 1)
        trip_end_date_str = trip_end_date.strftime("%Y-%m-%d")

        url = f"http://www.di-srv.unisa.it/~ads/corso-security/www/CORSO-0304/PAROS/http.htm"

        #print(url)

        # Visita l'URL
        driver.get(url)

        # Attendi che la pagina dei risultati dei voli venga caricata completamente
        #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")))

        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='title is--large has-text-white not-editable']")))


        print(element.text)


    

    # Chiudi il WebDriver
    driver.quit()


#Informazioni proxy
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://sslproxies.org/")
driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered']//th[contains(., 'IP Address')]"))))
ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 1]")))]
ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 2]")))]
driver.quit()
proxies = []
for i in range(0, len(ips)):
    proxies.append(ips[i]+':'+ports[i])
print(proxies)

# Impostazioni per lo scraping
origin = "ROMA"
destination = ["NYCA", "LAXA", "MIAA", "CHIA", "CAI", "NBOA", "BUEA", "RIOA", "MEXA", "CPT", "RAK", "DXB", "IST"]
trip_duration = 5
start_date = datetime(2024, 8, 13)
end_date = datetime(2024, 8, 25)

# Esegui lo scraping

for index, dest in enumerate(destination):
    scrape_skyscanner(origin, dest, trip_duration, start_date, end_date, proxies[index])
