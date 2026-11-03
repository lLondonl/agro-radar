import requests

url = "https://www.cbr-xml-daily.ru/daily_json.js"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    print("Не удалось получить курсы:", e)
    data = None

if data:
    print("Код ответа:", response.status_code)
    rates = {}
    for code in ["USD", "EUR", "CNY"]:
        v = data["Valute"][code]
        rate = v["Value"] / v["Nominal"]
        prev = v["Previous"] / v["Nominal"]
        rates[code] = rate
        arrow = "▲" if rate > prev else "▼"
        print(f"{v['Name']}: {rate:.2f} руб {arrow} (было {prev:.2f})")

    while True:
        text = input("\nЦена тонны, руб: ").replace(",", ".").replace(" ", "")
        try:
            price = float(text)
            break
        except ValueError:
            print("Нужно число, например 13500")

    print(f"В долларах: {price / rates['USD']:,.2f} $")
    print(f"В юанях:    {price / rates['CNY']:,.2f} ¥")
    print(f"В евро:     {price / rates['EUR']:,.2f} €")