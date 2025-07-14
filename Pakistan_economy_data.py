import requests
import pandas as pd

# --- Configuration ---
countries = {
    'Pakistan': 'PAK',
    'India': 'IND',
    'Bangladesh': 'BGD'
}

indicators = {
    'GDP': 'NY.GDP.MKTP.CD',
    'Inflation': 'FP.CPI.TOTL.ZG',
    'Unemployment': 'SL.UEM.TOTL.ZS',
    'School Enrollment': 'SE.PRM.ENRR',
    'CO2 Emissions': 'EN.ATM.CO2E.PC'
}

final_data = []

# --- Loop through countries and indicators ---
for country_name, country_code in countries.items():
    for metric_name, indicator_code in indicators.items():
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date=2000:2022&format=json&per_page=1000"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            if len(json_data) > 1 and json_data[1] is not None:
                for entry in json_data[1]:
                    if entry['value'] is not None:
                        final_data.append({
                            'Country': country_name,
                            'Year': int(entry['date']),
                            'Indicator': metric_name,
                            'Value': entry['value']
                        })
            else:
                print(f"⚠️ No data found for {country_name} - {metric_name}")
        else:
            print(f"❌ Request failed for {country_name} - {metric_name} (Status {response.status_code})")

# --- Convert to DataFrame ---
df = pd.DataFrame(final_data)

# --- Pivot to wide format ---
pivot_df = df.pivot_table(index=['Country', 'Year'], columns='Indicator', values='Value').reset_index()

# --- Save to CSV ---
pivot_df.to_csv("pakistan_economy_data_clean.csv", index=False)
print("✅ Data saved to 'pakistan_economy_data_clean.csv'")
