from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from myapp.models import Car

def index(request):
    response = ''
    response = json.dumps([{}])
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(response, content_type='text/json')

def get_car(request, car_name):
    response = ''
    if request.method == 'GET':
        try:
            car = Car.objects.get(name=car_name)
            response = json.dumps([{ 'Car': car.name, 'Top_Speed': car.top_speed}])
        except:
            response = json.dumps([{ 'Error': 'No car with that name'}])
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(response, content_type='text/json')

def get_all_cars(request):
    cars = []
    if request.method == 'GET':
        try:
            car_lists = Car.objects.all()
            for car in car_lists:
                cars.append({ 'Car': car.name, 'Top_Speed': car.top_speed})
            response = json.dumps(cars)
        except:
            response = json.dumps([{ 'Error': 'Could not retrieve all data.'}])

    response['Access-Control-Allow-Origin'] = '*' 
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def add_car(request):
    response = ''
    if request.method == 'POST':
        payload = json.loads(request.body)
        car_name = payload['name']
        top_speed = payload['top_speed']
        car = Car(name=car_name, top_speed=top_speed)

        # If the car record already exists, update it.
        if(Car.objects.filter(name=car_name).count() > 0):
            #Car.objects.filter(name=car_name).update(top_speed = top_speed)
            response = json.dumps([{ 'Error': '같은 단어가 반복되었습니다!'}])

        elif(not check_if_words_valid(Car.objects.all().latest("id").name, car_name)):
            response = json.dumps([{ 'Error': '제대로 된 끝말잇기를 해주세요.'}])

        # Else, insert it.
        else:
            try:
                car.save()
                response = json.dumps([{ 'Success': 'Car added successfully!'}])
            except:
                response = json.dumps([{ 'Error': 'Car could not be added!'}])
    return HttpResponse(response, content_type='text/json')


def check_if_words_valid(first_word, second_word):
    if first_word[-1] == second_word[0]:
        return True
    else:
        return False
