import requests
import json
import csv
import datetime
import time

# Verkrijg de JSON data
response = requests.get("http://fiets.openov.nl/locaties.json")
data = response.json()

# Haal de nodige informatie op
extracted_data = []
for key, location in data['locaties'].items():
    description = location.get('description', '')
    location_code = location.get('extra', {}).get('locationCode', '')
    rental_bikes = location.get('extra', {}).get('rentalBikes', '')
    fetch_time = location.get('extra', {}).get('fetchTime', '')
    open_status = location.get('open', '')
    extracted_data.append([description, location_code, rental_bikes, fetch_time, open_status])

# Maak de map 'scrapes' als deze nog niet bestaat
os.makedirs('scrapes', exist_ok=True)

# Maak een CSV bestandsnaam met de huidige tijd als Unix Timestamp
current_time = int(time.time())
filename = os.path.join(os.getcwd(), 'scrapes', f"beschikbaarheid_ov-fietsen_{current_time}.csv")

# Schrijf de gegevens naar een CSV-bestand
with __builtins__.open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "open"])
    writer.writerows(extracted_data)

print(f"Data geschreven naar {filename}")
