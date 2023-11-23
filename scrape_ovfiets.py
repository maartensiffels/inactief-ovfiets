import requests
import json
import csv
import datetime
import time
import os

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

# Haal de huidige directory op waar het script wordt uitgevoerd
current_dir = os.getcwd()

# Schrijf de gegevens naar een CSV-bestand in de map 'scrapes'
scrapes_dir = os.path.join(current_dir, 'scrapes')
os.makedirs(scrapes_dir, exist_ok=True)
filename = f"scrapes/beschikbaarheid_ov-fietsen_{int(time.time())}.csv"
with open(os.path.join(current_dir, filename), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
    writer.writerows(extracted_data)

print(f"Data geschreven naar {filename}")

# Schrijf de gegevens per maand naar afzonderlijke CSV-bestanden
for row in extracted_data:
    # Zorg ervoor dat fetch_time een string is die een datum en tijd representeert
    fetch_time = datetime.datetime.fromtimestamp(int(row[3])).strftime('%Y-%m-%d %H:%M:%S')
    fetch_date = datetime.datetime.strptime(fetch_time, '%Y-%m-%d %H:%M:%S')
    monthly_filename = f"beschikbaarheid_ov-fietsen_{fetch_date.year}_{fetch_date.month}.csv"
    monthly_file_path = os.path.join(current_dir, monthly_filename)
    # Check of het maandelijkse bestand al bestaat, zo niet maak dan een nieuwe met headers
    file_exists = os.path.isfile(monthly_file_path)
    with open(monthly_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
        writer.writerow(row)

    print(f"Data geschreven naar {monthly_filename}")
