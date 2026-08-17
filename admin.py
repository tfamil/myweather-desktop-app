# Name:           [Your Full Name]
# Student Number: [Your Student Number]

import json
import urllib.request
import urllib.parse
import webbrowser
from pprint import pp

API_KEY = '92117804ca1272872f70367fe81b78ea'


def input_something(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value


def format_location(location):
    if 'state' in location:
        return f"{location['name']}, {location['state']}, {location['country']}"
    return f"{location['name']}, {location['country']}"


def select_option(prompt, options):
    while True:
        try:
            choice = int(input(prompt + ' '))
            if choice == 0:
                return False
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        print(f'Please enter a number between 0 and {len(options)}.')


def save_data(data):
    file = open('locations.txt', 'w')
    json.dump(data, file, indent=4)
    file.close()


try:
    file = open('locations.txt', 'r')
    data = json.load(file)
    file.close()
except Exception:
    data = []

print('Welcome to the Weather App Admin Program.')

while True:
    print('\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.')
    choice = input('> ').lower()

    if choice == 'a':
        city_name = input_something('Enter a city/town name: ')

        encoded = urllib.parse.quote(city_name)
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={encoded}&limit=4&appid={API_KEY}'
        with urllib.request.urlopen(url) as response:
            results = json.loads(response.read().decode())

        if not results:
            print('No matching locations.')
        else:
            print('Matching location(s) found:')
            for i, location in enumerate(results, 1):
                print(f' {i}) {format_location(location)}')

            selected = select_option('Which one do you want to add?', results)

            if selected is not False:
                new_location = {
                    'name': selected['name'],
                    'country': selected['country'],
                    'lat': round(selected['lat'], 6),
                    'lon': round(selected['lon'], 6)
                }
                if 'state' in selected and selected['state']:
                    new_location['state'] = selected['state']

                data.append(new_location)
                save_data(data)
                print('Location added.')

    elif choice == 'l':
        if not data:
            print('No locations saved.')
        else:
            print('List of locations:')
            for i, location in enumerate(data, 1):
                print(f' {i}) {format_location(location)}')

    elif choice == 's':
        if not data:
            print('No locations saved.')
        else:
            search_term = input_something('Enter search term: ')
            matches = []
            for i, location in enumerate(data):
                if search_term.lower() in format_location(location).lower():
                    matches.append((i + 1, location))
            if not matches:
                print('No results found.')
            else:
                print('Search results:')
                for num, location in matches:
                    print(f' {num}) {format_location(location)}')

    elif choice == 'v':
        if not data:
            print('No locations saved.')
        else:
            selected = select_option('Location number to view:', data)
            if selected is not False:
                print(f' {format_location(selected)}')
                print(f' Coordinates: {selected["lat"]}, {selected["lon"]}')

    elif choice == 'd':
        if not data:
            print('No locations saved.')
        else:
            selected = select_option('Location number to delete:', data)
            if selected is not False:
                data.remove(selected)
                save_data(data)
                print('Location deleted.')

    elif choice == 'q':
        print("Goodbye!  Thank you for using [Your Full Name]'s ([Your Student Number]) admin program.")
        break

    else:
        print('Invalid choice.')