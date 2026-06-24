import customtkinter as ctk
import threading
import pyperclip
from weather import get_temp_from_timeanddate, slug

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Weather App")
app.geometry("500x380")
app.minsize(500, 380)

def update_result(text):
    result_label.configure(text=text)
    status_label.configure(text="Ready")
    weather_button.configure(state="normal")

def fetch_weather():
    city = city_entry.get().strip()
    country = country_entry.get().strip() or "india"

    if not city:
        update_result("⚠️ Please enter a city")
        return

    weather_button.configure(state="disabled")
    status_label.configure(text="Fetching weather...")

    try:
        temp, err = get_temp_from_timeanddate(
            slug(country),
            slug(city)
        )

        if temp:
            result = (
                f"🌦️ Weather Report\n\n"
                f"City: {city.title()}\n"
                f"Country: {country.title()}\n\n"
                f"{temp}"
            )
        else:
            result = f"❌ {err}"

        app.after(0, lambda: update_result(result))

    except Exception as e:
        app.after(
            0,
            lambda: update_result(f"❌ Error: {e}")
        )

def show_weather():
    threading.Thread(
        target=fetch_weather,
        daemon=True
    ).start()

def copy_result():
    text = result_label.cget("text")

    if text:
        pyperclip.copy(text)
        status_label.configure(text="Copied to clipboard")

def clear_fields():
    city_entry.delete(0, "end")
    country_entry.delete(0, "end")
    result_label.configure(text="")
    status_label.configure(text="Ready")

title_label = ctk.CTkLabel(
    app,
    text="🌍 Weather App",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=(20, 10))

city_entry = ctk.CTkEntry(
    app,
    width=350,
    height=40,
    placeholder_text="Enter City"
)
city_entry.pack(pady=8)

country_entry = ctk.CTkEntry(
    app,
    width=350,
    height=40,
    placeholder_text="Enter Country (default: India)"
)
country_entry.pack(pady=8)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=15)

weather_button = ctk.CTkButton(
    button_frame,
    text="Get Weather",
    width=120,
    command=show_weather
)
weather_button.pack(side="left", padx=5)

copy_button = ctk.CTkButton(
    button_frame,
    text="Copy",
    width=100,
    command=copy_result
)
copy_button.pack(side="left", padx=5)

clear_button = ctk.CTkButton(
    button_frame,
    text="Clear",
    width=100,
    command=clear_fields
)
clear_button.pack(side="left", padx=5)

result_label = ctk.CTkLabel(
    app,
    text="",
    justify="left",
    wraplength=430,
    font=("Arial", 15)
)
result_label.pack(pady=20)

status_label = ctk.CTkLabel(
    app,
    text="Ready",
    text_color="gray"
)
status_label.pack(side="bottom", pady=10)

city_entry.bind("<Return>", lambda e: show_weather())
country_entry.bind("<Return>", lambda e: show_weather())

app.mainloop()
