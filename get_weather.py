import time
import requests
import config


def parse(json_weather):
    cloud = json_weather['weather'][0]['description']
    city_name = json_weather['name']
    tp = str(round((json_weather['main']['temp'] - 273.15), 2))
    fl_tp = str(round((json_weather['main']['feels_like'] - 273.15), 2))
    tm_sr = time.ctime((json_weather['sys']['sunrise']))
    tm_ss = time.ctime((json_weather['sys']['sunset']))
    temp = 'Real temperature - {} °C'.format(tp)
    feels_temp = 'Feels like - {} °C'.format(fl_tp)
    time_sunr = 'Sunrise - {}'.format(tm_sr)
    time_suns = 'Sunset - {}'.format(tm_ss)
    return '{}\n{}\n{}\n{}\n{}\n{}'.format(city_name, cloud.capitalize(), feels_temp, temp, time_sunr, time_suns)


def get_weather_info(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_key}'
        r = requests.get(url)
        if r.status_code == 200:
            return parse(r.json())
        else:
            return 'Wrong city. Try again!'
    except NameError:
        return 'NameError'
