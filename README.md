# Skyscanner_scraper

Skyscanner scraper is a Python tool to find the best travel prices between a departure city and a list of destinations within a specified period of time.

## Prerequisites

Before using the script, make sure you meet the following prerequisites:

- **Selenium**: Selenium needs to be installed. You can install it by running the following command:
```bash
pip install selenium==3.141.0
```

## Usage

You can use the scraper_proxy.py to find prices between a departure city and a list of destinations within a specified period of time. It will use proxies to change IP address.

```python
origin = "ROME"
destination = ["NYCA", "LAXA", "MIAA", "CHIA", "CAI", "NBOA", "BUEA", "RIOA", "MEXA", "CPT", "RAK", "DXB", "IST"]
trip_duration = 4
start_date = datetime(2024, 4, 25)
end_date = datetime(2024, 8, 30)
```

Also you can use the script nordvpn_switcher_linux.py that works in a different way. 
In this case, the script switches the country it connects to using NordVPN and finds the best price with that VPN.
It's important to have NordVPN connected through the command line beforehand. This script utilizes commands that are compatible with the Linux operating system.



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

