import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


API_KEY = "7c2e450e07c546f4b072a9b76c64fc12" 
CITY = "Ujjain"
UNITS = "imperial" 


def fetch_weather(city, api_key, units="metric"):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    return response.json()

def process_data(data):
    timestamps = []
    temperatures = []
    humidities = []
    wind_speeds = []

    for entry in data["list"]:
        dt = datetime.fromtimestamp(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]

        timestamps.append(dt)
        temperatures.append(temp)
        humidities.append(humidity)
        wind_speeds.append(wind_speed)

    return timestamps, temperatures, humidities, wind_speeds

def create_dashboard(timestamps, temps, hums, winds, city):
    sns.set(style="darkgrid")
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(f"5-Day Weather Forecast for {city}", fontsize=16)

    axes[0].plot(timestamps, temps, color="tomato", marker='o')
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].set_title("Temperature Over Time")

    axes[1].plot(timestamps, hums, color="skyblue", marker='s')
    axes[1].set_ylabel("Humidity (%)")
    axes[1].set_title("Humidity Over Time")

    axes[2].plot(timestamps, winds, color="seagreen", marker='^')
    axes[2].set_ylabel("Wind Speed (m/s)")
    axes[2].set_title("Wind Speed Over Time")
    axes[2].set_xlabel("Date and Time")

    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def main():
    print(f"Fetching weather data for {CITY}...")
    try:
        raw_data = fetch_weather(CITY, API_KEY, UNITS)
        timestamps, temps, hums, winds = process_data(raw_data)
        create_dashboard(timestamps, temps, hums, winds, CITY)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
