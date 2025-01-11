import csv
import requests
from datetime import datetime

# API details
API_URL = "https://analytics.api.aiesec.org/v2/applications/analyze.json"
ACCESS_TOKEN = "RXBUGkKFVOodLmUrtvEni1dgj_vwQ8sVcQYJpGhnUx4"  # used the dirty method form console, waiting to get my own access token
OFFICE_ID = 1623  # Office ID for AIESEC in Sri Lanka
PROGRAM_ID = 7  # iGV program ID
START_DATE = "2024-02-14"
END_DATE = "2024-07-31"
OUTPUT_FILE = "iGV_analytics_sri_lanka.csv"

# Function to fetch data from the API
def fetch_analytics():
    params = {
        "histogram[office_id]": OFFICE_ID,
        "histogram[type]": "opportunity",
        "histogram[interval]": "month",
        "start_date": START_DATE,
        "end_date": END_DATE,
        "programmes[]": PROGRAM_ID,
        "access_token": ACCESS_TOKEN,
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

# Function to process and extract data
def process_data(api_response):
    if not api_response:
        print("No API response received.")
        return []

    data = api_response.get("analytics", {})
    approvals = data.get("total_approvals", {}).get("applications", {}).get("buckets", [])
    realizations = data.get("total_realized", {}).get("applications", {}).get("buckets", [])

    results = []

    for i in range(len(approvals)):
        month = approvals[i]["key_as_string"]
        approvals_count = approvals[i]["doc_count"]
        realized_count = realizations[i]["doc_count"] if i < len(realizations) else 0

        formatted_month = datetime.strptime(month, "%Y-%m-%d").strftime("%B %Y")

        results.append({
            "Month": formatted_month,
            "Approvals": approvals_count,
            "Realizations": realized_count
        })

    return results

# Function to write data to CSV
def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV.")
        return

    headers = data[0].keys()

    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Main function
def main():
    print("Fetching data from API...")
    api_response = fetch_analytics()

    print("Processing data...")
    processed_data = process_data(api_response)

    print(f"Writing data to {OUTPUT_FILE}...")
    write_to_csv(processed_data, OUTPUT_FILE)

    print("Process completed successfully.")

# Run the script
if __name__ == "__main__":
    main()
