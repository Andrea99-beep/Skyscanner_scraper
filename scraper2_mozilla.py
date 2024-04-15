from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
import random 
import geckodriver_autoinstaller
from webdriver_manager.firefox import GeckoDriverManager


def scrape_skyscanner(origin, destination, trip_duration, start_date, end_date, proxy):
    options = Options()
    options.add_argument('--proxy-server={}'.format(proxy))

    #driver = webdriver.Firefox(service=FirefoxService(executable_path="geckodriver_path"), options=options)
    driver = webdriver.Firefox(executable_path="C:\\Users\\Andrea\\Download\\geckodriver-v0.34.0-win-aarch64\\geckodriver.exe", options=options)
    driver.maximize_window()

    volo_migliore = []
    volo_economico = []
    volo_migliore_date = []
    volo_economico_date = []

    while start_date + timedelta(days=5) <= end_date:
        trip_end_date = start_date + timedelta(days=trip_duration - 1)
        trip_end_date_str = trip_end_date.strftime("%Y-%m-%d")

        url = f"https://www.skyscanner.it/trasporti/voli/{origin}/{destination}/{start_date_str}/{trip_end_date_str}/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1"

        driver.get(url)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")))

        flight_options = driver.find_elements_by_css_selector(".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")

        for index, option  in enumerate(flight_options):
            if index == 0:
                volo_migliore.append(int(option.text.strip('€').replace(".", "")))
                volo_migliore_date.append((start_date_str, trip_end_date_str))
            elif index == 1:
                volo_economico.append(int(option.text.strip('€').replace(".", "")))
                volo_economico_date.append((start_date_str, trip_end_date_str))
            else:
                break

        start_date += timedelta(days=1)
        start_date_str = start_date.strftime("%Y-%m-%d")

    min_volo_migliore_index = volo_migliore.index(min(volo_migliore))
    min_volo_economico_index = volo_economico.index(min(volo_economico))

    print("Destinazione: " + destination)
    print("Prezzo migliore:", min(volo_migliore), "Date:", volo_migliore_date[min_volo_migliore_index])
    print("Prezzo più economico:", min(volo_economico), "Date:", volo_economico_date[min_volo_economico_index])

    driver.quit()

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Firefox(executable_path="C:\\Users\\Andrea\\Download\\geckodriver-v0.34.0-win-aarch64\\geckodriver.exe", options=options)
driver.get("https://sslproxies.org/")
driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered']//th[contains(., 'IP Address')]"))))
ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 1]")))]
ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 2]")))]
driver.quit()
proxies = []
for i in range(0, len(ips)):
    proxies.append(ips[i]+':'+ports[i])
print(proxies)

origin = "ROMA"
destination = ["NYCA", "LAXA", "MIAA", "CHIA", "CAI", "NBOA", "BUEA", "RIOA", "MEXA", "CPT", "RAK", "DXB", "IST"]
trip_duration = 5
start_date = datetime(2024, 8, 13)
end_date = datetime(2024, 8, 25)

lunghezza = len(proxies)

for index, dest in enumerate(destination):
    scrape_skyscanner(origin, dest, trip_duration, start_date, end_date, proxies[random.randint(0,lunghezza-1)])
