import requests
import csv
import datetime
import os
from collections import defaultdict

# Verkrijg de JSON data
response = requests.get("http://fiets.openov.nl/locaties.json")
data = response.json()

# Haal de nodige informatie op en groepeer deze per maand
monthly_data = defaultdict(list)
for key, location in data['locaties'].items():
    description = location.get('description', '')
    location_code = location.get('extra', {}).get('locationCode', '')
    rental_bikes = location.get('extra', {}).get('rentalBikes', '')
    fetch_time = location.get('extra', {}).get('fetchTime', '')
    loc_type = location.get('extra', {}).get('type', '')
    open_status = location.get('open', '')
    
    # Converteer fetch_time naar een datetime object en formatteer naar "YYYY-MM"
    fetch_time_datetime = datetime.datetime.fromtimestamp(int(fetch_time))
    month_year = fetch_time_datetime.strftime("%Y-%m")
    
    monthly_data[month_year].append([description, location_code, rental_bikes, fetch_time, loc_type, open_status])

# Haal de huidige directory op waar het script wordt uitgevoerd
current_dir = os.getcwd()

# Controleer of de scrapes directory bestaat, maak deze anders aan
scrapes_dir = os.path.join(current_dir, 'scrapes')
if not os.path.exists(scrapes_dir):
    os.makedirs(scrapes_dir)

# Schrijf de gegevens naar een CSV-bestand per maand
for month_year, data in monthly_data.items():
    filename = os.path.join(scrapes_dir, f"beschikbaarheid_ov-fietsen_{month_year}.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["description", "locationCode", "rentalBikes", "fetchTime", "type", "open"])
        writer.writerows(data)
    print(f"Data geschreven naar {filename}")

# (Optioneel) Voeg de nieuwe gegevens toe aan het 'master' CSV-bestand per maand
# Deze stap zou afhankelijk zijn van hoe u de 'master' bestanden georganiseerd wilt hebben.
