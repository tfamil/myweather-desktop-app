# Name:           [Your Full Name]
# Student Number: [Your Student Number]

import tkinter
import tkinter.messagebox
import json
import urllib.request
import datetime
import os
# Reference: https://pillow.readthedocs.io/en/stable/reference/ImageTk.html
from PIL import ImageTk, Image


API_KEY = '92117804ca1272872f70367fe81b78ea'

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


def degrees_to_cardinal(degrees):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # Reference: https://stackoverflow.com/a/7490772
    return directions[round(degrees / 45) % 8]


def unix_to_local_time(unix_timestamp, tz_offset_seconds):
    # Reference: https://docs.python.org/3/library/datetime.html#datetime.timezone
    tz = datetime.timezone(datetime.timedelta(seconds=tz_offset_seconds))
    dt = datetime.datetime.fromtimestamp(unix_timestamp, tz=tz)
    return dt.strftime('%I:%M%p')


class ProgramGUI:
    def __init__(self):
        try:
            file = open('locations.txt', 'r')
            self.data = json.load(file)
            file.close()
        except Exception:
            tkinter.messagebox.showerror('MyWeather', 'Missing/Invalid file')
            return

        if not self.data:
            tkinter.messagebox.showerror('MyWeather', 'No locations found. Please add locations using admin.py first.')
            return

        self.index = 0

        self.window = tkinter.Tk()
        self.window.title('MyWeather')
        self.window.geometry('420x270+98+98')
        self.window.resizable(False, False)
        self.window.configure(bg='#87CEEB')

        # Navigation row:  <   Name   >
        nav_frame = tkinter.Frame(self.window, bg='#87CEEB')
        nav_frame.pack(fill='x', padx=8, pady=(10, 0))

        self.btn_prev = tkinter.Button(nav_frame, text='<', command=self.previous,
                                       bg='#87CEEB', fg='black', relief='flat',
                                       font=('Arial', 14, 'bold'), padx=6)
        self.btn_prev.pack(side='left')

        self.lbl_name = tkinter.Label(nav_frame, text='', bg='#87CEEB', fg='black',
                                      font=('Arial', 20, 'bold'))
        self.lbl_name.pack(side='left', expand=True)

        self.btn_next = tkinter.Button(nav_frame, text='>', command=self.next,
                                       bg='#87CEEB', fg='black', relief='flat',
                                       font=('Arial', 14, 'bold'), padx=6)
        self.btn_next.pack(side='right')

        # State / country
        self.lbl_region = tkinter.Label(self.window, text='', bg='#87CEEB', fg='black',
                                        font=('Arial', 11))
        self.lbl_region.pack()

        # Description text + icon on same row
        desc_frame = tkinter.Frame(self.window, bg='#87CEEB')
        desc_frame.pack(pady=(10, 6))

        self.lbl_description = tkinter.Label(desc_frame, text='', bg='#87CEEB', fg='black',
                                             font=('Arial', 18, 'bold'))
        self.lbl_description.pack(side='left', padx=(12, 6))

        first_icon = Image.open(os.path.join(IMAGES_DIR, '01d.png'))
        self.photo = ImageTk.PhotoImage(first_icon)
        self.lbl_icon = tkinter.Label(desc_frame, image=self.photo, bg='#87CEEB')
        self.lbl_icon.pack(side='left')

        # Temperature / feels like / humidity  (single line)
        self.lbl_temp = tkinter.Label(self.window, text='', bg='#87CEEB', fg='black',
                                      font=('Arial', 11))
        self.lbl_temp.pack()

        # Wind (single line)
        self.lbl_wind = tkinter.Label(self.window, text='', bg='#87CEEB', fg='black',
                                      font=('Arial', 11))
        self.lbl_wind.pack()

        # Sunrise / sunset (single line)
        self.lbl_sun = tkinter.Label(self.window, text='', bg='#87CEEB', fg='black',
                                     font=('Arial', 11))
        self.lbl_sun.pack()

        self.show_weather()
        tkinter.mainloop()


    def show_weather(self):
        location = self.data[self.index]

        if 'data' not in location:
            url = (f'https://api.openweathermap.org/data/2.5/weather'
                   f'?lat={location["lat"]}&lon={location["lon"]}'
                   f'&units=metric&appid={API_KEY}')
            with urllib.request.urlopen(url) as response:
                location['data'] = json.loads(response.read().decode())

        weather = location['data']

        # Location name and region
        self.lbl_name.configure(text=location['name'])
        if 'state' in location:
            region = f"{location['state']}, {location['country']}"
        else:
            region = location['country']
        self.lbl_region.configure(text=region)

        # Icon
        icon_code = weather['weather'][0]['icon']
        icon_path = os.path.join(IMAGES_DIR, f'{icon_code}.png')
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            self.photo = ImageTk.PhotoImage(img)
            self.lbl_icon.configure(image=self.photo)

        # Description
        description = weather['weather'][0]['description'].capitalize()
        self.lbl_description.configure(text=description)

        # Temperature line:  24.3°C (feels like 23.9°C), 42% humidity.
        main = weather['main']
        temp      = round(main['temp'], 1)
        feels     = round(main['feels_like'], 1)
        humidity  = main['humidity']
        self.lbl_temp.configure(text=f'{temp}°C (feels like {feels}°C), {humidity}% humidity.')

        # Wind line:  Winds NE at 22.4km/h (gusts 28.9km/h).
        wind      = weather['wind']
        speed_kmh = round(wind['speed'] * 3.6, 1)
        direction = degrees_to_cardinal(wind['deg']) if 'deg' in wind else ''
        if 'gust' in wind:
            gust_kmh = round(wind['gust'] * 3.6, 1)
            wind_str = f'Winds {direction} at {speed_kmh}km/h (gusts {gust_kmh}km/h).'
        else:
            wind_str = f'Winds {direction} at {speed_kmh}km/h.'
        self.lbl_wind.configure(text=wind_str)

        # Sunrise / sunset line:  Sunrise 05:37AM, Sunset 07:21PM
        tz_offset = weather['timezone']
        sunrise   = unix_to_local_time(weather['sys']['sunrise'], tz_offset)
        sunset    = unix_to_local_time(weather['sys']['sunset'],  tz_offset)
        self.lbl_sun.configure(text=f'Sunrise {sunrise}, Sunset {sunset}')


    def previous(self):
        if self.index > 0:
            self.index -= 1
            self.show_weather()


    def next(self):
        if self.index < len(self.data) - 1:
            self.index += 1
            self.show_weather()


gui = ProgramGUI()