# weather.py
# Simple scraper for timeanddate.com (prints current temperature)
import requests
from bs4 import BeautifulSoup

def slug(s: str) -> str:
    return s.strip().lower().replace(' ', '-')

def get_temp_from_timeanddate(country_slug, city_slug):
    url = f"https://www.timeanddate.com/weather/{country_slug}/{city_slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        return None, f"Network error: {e}"

    if resp.status_code != 200:
        return None, f"Bad response: {resp.status_code} for URL {url}"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Main quick-look box normally has id="qlook"
    qlook = soup.find("div", id="qlook")
    if qlook:
        temp_div = qlook.find("div", class_="h2")
        desc = qlook.find("p")
    else:
        # fallback: try to find any div with class h2
        temp_div = soup.find("div", class_="h2")
        desc = None

    if temp_div:
        temp_text = temp_div.get_text(strip=True)
        desc_text = desc.get_text(strip=True) if desc else ""
        return f"{temp_text} {desc_text}".strip(), None

    # If we reach here, we couldn't find the temperature
    return None, "Couldn't find temperature on the page. Maybe the city/country is wrong or site layout changed."

def main():
    print("== Local Weather CLI (timeanddate.com) ==")
    city = input("City (e.g., Kochi): ").strip()
    if not city:
        print("You must enter a city. Exiting.")
        return
    country = input("Country (e.g., india) [press Enter for 'india']: ").strip() or "india"

    cslug = slug(country)
    cityslug = slug(city)

    temp, err = get_temp_from_timeanddate(cslug, cityslug)
    if temp:
        print(f"Current in {city.title()}, {country.title()}: {temp}")
    else:
        print("Error:", err)
        print("Tip: If this fails, try entering the 'full URL' of the timeanddate page for your city instead.")
        print("Example URL format: https://www.timeanddate.com/weather/india/kochi")

if __name__ == "__main__":
    main()
