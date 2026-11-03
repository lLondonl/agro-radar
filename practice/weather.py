import requests

params = {
    "latitude": 45.04,
    "longitude": 41.97,
    "daily": "precipitation_sum,temperature_2m_max",
    "timezone": "Europe/Moscow",
    "forecast_days": 5,
}
r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
r.raise_for_status()
daily = r.json()["daily"]

for day, rain, temp in zip(daily["time"], daily["precipitation_sum"], daily["temperature_2m_max"]):
    note = "дождь — погрузка под вопросом" if rain >= 2 else "сухо"
    print(f"{day}: до {temp:.0f}°, осадки {rain} мм — {note}")