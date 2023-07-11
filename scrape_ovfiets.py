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
    loc_type = location.get('extra', {}).get('type', '')
    open_status = location.get('open', '')
    extracted_data.append([description, location_code, rental_bikes, fetch_time, loc_type, open_status])

# Maak een CSV bestandsnaam met de huidige tijd als Unix Timestamp
current_time = int(time.time())
filename = f"beschikbaarheid_ov-fietsen_{current_time}.csv"

# Schrijf de gegevens naar een CSV-bestand
with __builtins__.open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
    writer.writerows(extracted_data)

print(f"Data geschreven naar {filename}")

# Voeg de nieuwe gegevens toe aan het 'master' CSV-bestand
with __builtins__.open("beschikbaarheid_ov-fietsen_master.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(extracted_data)

print("Data toegevoegd aan beschikbaarheid_ov-fietsen_master.csv")
