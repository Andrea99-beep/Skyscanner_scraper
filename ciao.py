import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_skyscanner(origin, destination, trip_duration, start_date, end_date):
    volo_migliore = []
    volo_economico = []
    volo_migliore_date = []
    volo_economico_date = []

    while start_date + timedelta(days=5) <= end_date:
        trip_end_date = start_date + timedelta(days=trip_duration - 1)

        url = f"https://www.skyscanner.it/trasporti/voli/{origin}/{destination}/{start_date.strftime('%Y-%m-%d')}/{trip_end_date.strftime('%Y-%m-%d')}/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1"

        response = requests.get(url)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')


            #flight_options = response.json()['BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN']
            #flight_options = soup.select(".BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")
            #flight_options = soup.select("span.BpkText_bpk-text__MWZkY.BpkText_bpk-text--heading-4__MzBkN")

            flight_options = soup.find_all("div", class_="FqsTabs_fqsTabsWithSparkle__ZDAyO")

            print(flight_options)


            for index, option in enumerate(flight_options):
                if index == 0:
                    volo_migliore.append(int(option['text'].strip('€').replace(".", "")))
                    volo_migliore_date.append((start_date.strftime('%Y-%m-%d'), trip_end_date.strftime('%Y-%m-%d')))
                elif index == 1:
                    volo_economico.append(int(option['text'].strip('€').replace(".", "")))
                    volo_economico_date.append((start_date.strftime('%Y-%m-%d'), trip_end_date.strftime('%Y-%m-%d')))
                else:
                    break

        start_date += timedelta(days=1)

    min_volo_migliore_index = volo_migliore.index(min(volo_migliore))
    min_volo_economico_index = volo_economico.index(min(volo_economico))

    print("Destinazione:", destination)
    print("Prezzo migliore:", min(volo_migliore), "Date:", volo_migliore_date[min_volo_migliore_index])
    print("Prezzo più economico:", min(volo_economico), "Date:", volo_economico_date[min_volo_economico_index])

# Impostazioni per lo scraping
origin = "ROMA"
destinations = ["NYCA", "LAXA", "MIAA", "CHIA", "CAI", "NBOA", "BUEA", "RIOA"]
trip_duration = 5
start_date = datetime(2024, 8, 13)
end_date = datetime(2024, 8, 25)

# Esegui lo scraping
for dest in destinations:
    scrape_skyscanner(origin, dest, trip_duration, start_date, end_date)
