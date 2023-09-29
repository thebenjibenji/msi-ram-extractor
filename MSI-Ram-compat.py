import requests
import csv
import time
import json

# tested in PY 3.10
# Initialise an empty list to store the data
data_list = []

# Loop through each page
max_page = 8  # You can change this based on the actual number of pages
for page in range(1, max_page + 1):
    url = f"https://www.msi.com/api/v1/product/support/panel?product=Z390-A-PRO&type=mem&page={page}&per_page=180&id=3&keyword=&order=desc&column=Supported%20Speed%20(MHz)"
    
    # Mimic a browser header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Wait 5 seconds for the API to respond
    time.sleep(5)
    
    # Parse the JSON response
    try:
        json_data = json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON on page {page}. Response content:\n{response.text}")
        continue
    
    # Extract the relevant data and append to the list
    try:
        ram_data = json_data['result']['downloads']['Memory by I5/I7/I9']['list']
        data_list.extend(ram_data)
    except KeyError as e:
        print(f"KeyError: {e} is not in JSON data. JSON data:\n{json_data}")
        continue

# Write the data to a CSV file
with open('msi_memory_support.csv', 'w', newline='') as csvfile:
    fieldnames = ["Vendor", "Model", "DDR", "SPD Speed (MHz)", "Supported Speed (MHz)", "Chipset", "Voltage (V)", "Sided", "Size (GB)", "1|2|4 DIMM"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in data_list:
        if isinstance(row, dict):
            writer.writerow(row)
        else:
            print(f"Skipping row because it is not a dictionary: {row}")
