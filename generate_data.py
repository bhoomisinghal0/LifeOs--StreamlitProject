import pandas as pd
import random
from datetime import datetime, timedelta

# List of apps and their categories
apps = [
    ("Instagram", "Social Media"),
    ("YouTube", "Entertainment"),
    ("VS Code", "Coding"),
    ("Chrome", "Education"),
    ("ChatGPT", "Education"),
    ("Spotify", "Entertainment"),
]

start_date = datetime(2026, 7, 18)

data = []

# Generate data for 14 days
for day in range(14):
    current_date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")

    # Create one row for each app
    for app_name, category in apps:
        minutes = random.randint(20, 240)

        data.append({
            "Date": current_date,
            "App_Name": app_name,
            "Category": category,
            "Minutes_Used": minutes
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("screentime.csv", index=False)

print("screentime.csv created successfully!")