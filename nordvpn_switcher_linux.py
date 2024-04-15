from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import subprocess, re, random

def getCountries():
    """
    This function will return a list of the current countries with available servers for your nordvpn account.
    """
    nord_output = subprocess.Popen(["nordvpn", "countries"], stdout=subprocess.PIPE)
    countries = re.split("[\t \n]", nord_output.communicate()[0].decode("utf-8"))
    while "" in countries:
        countries.remove("")
    return countries

def scrape_skyscanner(origin, destination, trip_duration, start_date, end_date, country):

    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')    
    # Inizializza il WebDriver per Chrome


    # Connessione VPN ad uno specifico paese
    cmd = ["nordvpn", "c", country]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    if "Whoops! We couldn't connect you" in o.decode('ascii'):
        print("not connected. Abort...")
        return 100000, 100000
    else:
        print("Connected to {}".format(country))
    
    # Costruisci l'URL per la ricerca su Skyscanner

    # Converti le date in oggetti datetime
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")


    volo_migliore = []
    volo_economico = []
    volo_migliore_date = []
    volo_economico_date = []

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    while start_date + timedelta(days=trip_duration) <= end_date:

        trip_end_date = start_date + timedelta(days=trip_duration - 1)
        trip_end_date_str = trip_end_date.strftime("%Y-%m-%d")

        url = f"https://www.skyscanner.it/trasporti/voli/{origin}/{destination}/{start_date_str}/{trip_end_date_str}/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1"

        #print(url)

        # Visita l'URL
        driver.get(url)

        # Attendi che la pagina dei risultati dei voli venga caricata completamente
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")))


        # Trova tutte le opzioni di volo disponibili
        flight_options = driver.find_elements_by_css_selector(".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")


        # Estrai e stampa le informazioni sui voli
        for index, option  in enumerate(flight_options):
            if index == 0:
                #print("Volo migliore " + option.text)
                #print(int(option.text.strip('€')))
                volo_migliore.append(int(option.text.strip('€').replace(".", "")))
                volo_migliore_date.append((start_date_str, trip_end_date_str))
            elif index == 1:
                #print("Volo più economico " + option.text)
                volo_economico.append(int(option.text.strip('€').replace(".", "")))
                volo_economico_date.append((start_date_str, trip_end_date_str))
            else:
                break

        start_date += timedelta(days=1)
        start_date_str = start_date.strftime("%Y-%m-%d")

    # Trova le date con il prezzo minimo per entrambi i voli
    min_volo_migliore_index = volo_migliore.index(min(volo_migliore))
    min_volo_economico_index = volo_economico.index(min(volo_economico))

    print("Destinazione: " + destination)
    print("Prezzo migliore:", min(volo_migliore), "Date:", volo_migliore_date[min_volo_migliore_index])
    print("Prezzo più economico:", min(volo_economico), "Date:", volo_economico_date[min_volo_economico_index])

    subprocess.call(["nordvpn", "disconnect"])
    print("Disconnected")

    # Chiudi il WebDriver
    driver.quit()

    return min(volo_migliore), min(volo_economico)

    

# Impostazioni per lo scraping
origin = "ROME"
destination = "CHIA"
trip_duration = 5
start_date = datetime(2024, 8, 13)
end_date = datetime(2024, 8, 18)
#countries = ['Norway', 'Sweden', 'Germany']

countries = getCountries()
del countries[:3]
print(countries)


results = []

# Esegui lo scraping
for country in countries:
    ris = scrape_skyscanner(origin, destination, trip_duration, start_date, end_date, country)
    results.append((country, ris[0], ris[1]))


print(results)

