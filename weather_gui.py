import customtkinter as ctk
from weather import get_temp_from_timeanddate, slug  # re-use your existing code

def show_weather():
    city = city_entry.get().strip()
    country = country_entry.get().strip() or "india"
    if not city:
        result_label.configure(text="⚠️ Enter a city")
        return

    cslug, ccity = slug(country), slug(city)
    temp, err = get_temp_from_timeanddate(cslug, ccity)
    if temp:
        result_label.configure(text=f"🌦️ {city.title()}, {country.title()}: {temp}")
    else:
        result_label.configure(text=f"❌ Error: {err}")

# --- UI Setup ---
ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Weather Widget")
app.geometry("350x250")

city_entry = ctk.CTkEntry(app, placeholder_text="Enter City (use valid name please)")
city_entry.pack(pady=10)

country_entry = ctk.CTkEntry(app, placeholder_text="Enter Country(use valid name)")
country_entry.pack(pady=10)

button = ctk.CTkButton(app, text="Get Weather", command=show_weather)
button.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
result_label.pack(pady=20)

app.mainloop()
