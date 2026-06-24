import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

def slug(text):
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text

def create_session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session

def fetch_page(session, url):
    for _ in range(3):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            return response.text, None
        except requests.RequestException as e:
            error = str(e)
    return None, error

def parse_weather(html):
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "temperature": "N/A",
        "condition": "N/A",
        "feels_like": "N/A",
        "humidity": "N/A",
        "wind": "N/A",
        "visibility": "N/A"
    }

    qlook = soup.find("div", id="qlook")

    if qlook:
        temp = qlook.find("div", class_="h2")
        desc = qlook.find("p")

        if temp:
            result["temperature"] = temp.get_text(" ", strip=True)

        if desc:
            result["condition"] = desc.get_text(" ", strip=True)

    table = soup.find("table")

    if table:
        rows = table.find_all("tr")

        for row in rows:
            cells = row.find_all(["th", "td"])

            if len(cells) < 2:
                continue

            key = cells[0].get_text(" ", strip=True).lower()
            value = cells[1].get_text(" ", strip=True)

            if "feels like" in key:
                result["feels_like"] = value

            elif "humidity" in key:
                result["humidity"] = value

            elif "wind" in key:
                result["wind"] = value

            elif "visibility" in key:
                result["visibility"] = value

    return result

def build_url(country, city):
    return f"https://www.timeanddate.com/weather/{slug(country)}/{slug(city)}"

def print_weather(city, country, weather):
    print("\n" + "=" * 60)
    print(f"Weather for {city.title()}, {country.title()}")
    print("=" * 60)

    print(f"Temperature : {weather['temperature']}")
    print(f"Condition   : {weather['condition']}")
    print(f"Feels Like  : {weather['feels_like']}")
    print(f"Humidity    : {weather['humidity']}")
    print(f"Wind        : {weather['wind']}")
    print(f"Visibility  : {weather['visibility']}")

    print("=" * 60)

def get_weather_from_url(url):
    parsed = urlparse(url)

    if "timeanddate.com" not in parsed.netloc:
        return None, "URL must be from timeanddate.com"

    session = create_session()

    html, error = fetch_page(session, url)

    if error:
        return None, error

    weather = parse_weather(html)

    return weather, None

def get_weather(country, city):
    session = create_session()

    url = build_url(country, city)

    html, error = fetch_page(session, url)

    if error:
        return None, error

    weather = parse_weather(html)

    return weather, None

def main():
    print("=" * 60)
    print("ADVANCED WEATHER CLI")
    print("=" * 60)

    mode = input(
        "\n1. Search by city\n2. Use full URL\n\nSelect (1/2): "
    ).strip()

    if mode == "2":
        url = input("\nEnter timeanddate URL: ").strip()

        if not url:
            print("No URL entered.")
            return

        weather, error = get_weather_from_url(url)

        if error:
            print(f"\nError: {error}")
            return

        print("\n" + "=" * 60)

        for key, value in weather.items():
            print(f"{key.replace('_', ' ').title():12}: {value}")

        print("=" * 60)

    else:
        city = input("\nCity: ").strip()

        if not city:
            print("City is required.")
            return

        country = input("Country [default: india]: ").strip() or "india"

        weather, error = get_weather(country, city)

        if error:
            print(f"\nError: {error}")
            print(
                f"Try visiting:\n{build_url(country, city)}"
            )
            return

        print_weather(city, country, weather)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
