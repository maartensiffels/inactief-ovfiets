import requests
import json
import csv
import datetime
import time
import os
from dateutil.parser import parse

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
filename = f"scrapes/beschikbaarheid_ov-fietsen_{current_time}.csv"

# Haal de huidige directory op waar het script wordt uitgevoerd
current_dir = os.getcwd()

# Controleer of de scrapes directory bestaat, maak deze anders aan
if not os.path.exists(os.path.join(current_dir, 'scrapes')):
    os.makedirs(os.path.join(current_dir, 'scrapes'))

# Schrijf de gegevens naar een CSV-bestand in de map 'scrapes'
with open(os.path.join(current_dir, filename), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
    writer.writerows(extracted_data)

print(f"Data geschreven naar {filename}")

# Voeg de nieuwe gegevens toe aan het 'master' CSV-bestand
#master_file_path = os.path.join(current_dir, "beschikbaarheid_ov-fietsen_master.csv")
#with open(master_file_path, 'a', newline='') as f:
#   writer = csv.writer(f)
#  writer.writerows(extracted_data)
#print("Data toegevoegd aan beschikbaarheid_ov-fietsen_master.csv")

# Schrijf de gegevens per maand naar afzonderlijke CSV-bestanden
for row in extracted_data:
    fetch_time = parse(row[3])  # Dit gebruikt de dateutil.parser om de tijd te parsen
    monthly_filename = f"beschikbaarheid_ov-fietsen_{fetch_time.year}_{fetch_time.month}.csv"
    monthly_file_path = os.path.join(current_dir, monthly_filename)
    # Check of het maandelijkse bestand al bestaat, zo niet maak dan een nieuwe met headers
    file_exists = os.path.isfile(monthly_file_path)
    with open(monthly_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
        writer.writerow(row)

    print(f"Data geschreven naar {monthly_filename}")
