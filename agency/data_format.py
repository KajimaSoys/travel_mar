from . import models
from django.db.models.functions import datetime
from datetime import datetime, timedelta
from num2words import num2words


def get_order_data(route, client):
    route_obj = models.Route.objects.filter(id=route).values()[0]
    worker = models.Worker.objects.filter(id=route_obj['worker_id']).values()[0]
    client_obj = models.Client.objects.filter(id=client).values()[0]
    route_points = models.RoutePoint.objects.filter(route=route).values()
    route_list = []
    for item in route_points:
        hotel = models.Hotel.objects.filter(id=item['hotel_id']).values()[0]
        item['hotel_name'] = hotel['name']
        item['hotel_type'] = hotel['type']
        item['hotel_address'] = hotel['address']
        route_list.append(item)

    obj = obj_container(route_obj, worker, client_obj, route_list)
    print(obj)
    return obj

def obj_container(route_obj, worker, client_obj, route_list):
    obj = []
    obj.extend([route_obj, worker, client_obj, route_list])
    return obj

def format(data):
    dict = {}

    route = data[0]
    dict['id'] = route['id']
    dict['routeName'] = route['routeName']
    dict['country'] = route['country']
    dict['period'] = route['period']
    dict['amount'] = route['amount']
    dict['returnCost'] = route['returnCost']
    dict['dateStart'] = datetime.strftime(route['dateStart'], "%d.%m.%Y")
    dict['dateStart_word'] = date2word(dict['dateStart'])
    dict['creation_date'] = datetime.strftime(route['creation_date'], "%d.%m.%Y")
    dict['creation_date_word'] = date2word(dict['creation_date'])

    worker = data[1]
    dict['worker_name'] = f"{worker['lastName']} {worker['firstName']} {worker['patronymic']}"
    temp = dict['worker_name'].split(' ')
    dict['worker_name_output'] = temp[0] + ' ' + temp[1][:1] + '.' + temp[2][:1] + '.'

    client = data[2]
    client_name = f"{client['lastName']} {client['firstName']} {client['patronymic']}"
    dict['client_name'] = client_name
    temp = client_name.split(' ')
    dict['client_name_output'] = temp[0] + ' ' + temp[1][:1] + '.' + temp[2][:1] + '.'
    dict['document'] = client['document']
    dict['serial'] = client['serial']
    dict['number'] = client['number']
    dict['date'] = datetime.strftime(client['date'], "%d.%m.%Y")
    dict['region'] = client['region']
    dict['born'] = datetime.strftime(client['born'], "%d.%m.%Y")
    if client['passport']:
        dict['passport'] = 'Имеет'
    else:
        dict['passport'] = 'Не имеет'
    dict['path'] = f'{temp[0]}{temp[1][:1]}.{temp[2][:1]}_{dict["id"]}'

    route_point = data[3]
    dict['towns'] = ""
    dict['comments'] = ""
    dict['hotels'] = ""
    for item in route_point:
        dict['towns'] = dict['towns'] + item['town'] + ', '
        dict['dateStop'] = datetime.strftime(item['stopDate'], "%d.%m.%Y")
        dict['comments'] = dict['comments'] + item['comment'] + ', '
        dict['hotels'] = dict['hotels'] + item['hotel_name'] + ' - ' + item['hotel_address'] + ', '
    dict['towns'] = dict['towns'][:-2]
    dict['comments'] = dict['comments'][:-2]
    dict['hotels'] = dict['hotels'][:-2]

    return dict


def date2word(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('.')
    date_list[1] = month_list[int(date_list[1]) - 1]
    return date_list


def n2w(num):
    return num2words(num, lang='ru')