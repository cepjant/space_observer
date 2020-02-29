from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import urllib.request
import json
from datetime import datetime
import folium


class Main(View):
    def get(self, request):
        ISS1 = ISS()
        map1 = Map()
        map1.create_map()
        crew = Crew()
        people_count, names_crafts, crew_message = crew.get_crew()
        date, time, ISS_message, position = ISS1.get_info()
        context = {
            'time': time,
            'date': date,
            'position': position,
            'ISS_message': ISS_message,
            'people_count': people_count,
            'names_crafts': names_crafts,
            'crew_message': crew_message
        }
        return render(request, 'main/index.html', context)


class ISS:
    def get_info(self):
        response = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
        obj = json.loads(response.read())
        date_time = (datetime.utcfromtimestamp(obj['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))
        date = date_time.split(' ')[0]
        time = date_time.split(' ')[1]
        if obj['message'] == 'success':
            message = 'Данные о позиции МКС получены.'
        else:
            message = 'Ошибка при получении данных о позиции МКС.'
        position = obj['iss_position']  # координаты МКС
        result = (date, time, message, position)
        return result


class Crew:
    def get_crew(self):
        response = urllib.request.urlopen("http://api.open-notify.org/astros.json")
        obj = json.loads(response.read())
        people_count = obj['number']
        names = []
        crafts = []
        for i in obj['people']:
            names.append(i['name'])
            crafts.append(i['craft'])
        names_crafts = dict(zip(names, crafts))  # формирование словаря {имя космонавта: корабль}
        if obj['message'] == 'success':
            message = 'Данные о составе экипажа получены.'
        else:
            message = 'Ошибки при получении данных о составе экипажа.'
        result = (people_count, names_crafts, message)
        return result


class Map:
    def create_map(self):
        ISS1 = ISS()
        lat, long = ISS1.get_info()[3]['latitude'], ISS1.get_info()[3]['longitude']  # получение широты и долготы МКС
        map = folium.Map(location=[37.143977, -121.963908], zoom_start=1,
                         tiles='CartoDB dark_matter')  # установка карты
        folium.CircleMarker(location=(lat, long), radius=9, popup='ISS',
                            fill_color='white', color="gray", fill_opacity=0.9).add_to(map)  # установка маркера МКС

        map.save('templates/map.html')  # сохранение карты в 'templates' проекта
