# coding=utf8
"""
openweather.py - Willie openweathermap.com module
"""
from __future__ import unicode_literals
from datetime import datetime
import json

from willie import web
from willie.module import commands, example


@commands('ow')
@example('.ow London')
def weather(bot, trigger):
    location = trigger.group(2)

    if not location:
        return bot.say("No location provided.")

    try:
        url = "http://api.openweathermap.org/data/2.5/weather?units=metric&q=" + location
        response = web.get(url, dont_decode=True)
    except Exception:
        return bot.say("Error while fetching data.")

    data = json.loads(response)
    if data["cod"] != 200:
        return bot.say(data["message"])

    name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    windspeed = data["wind"]["speed"]
    condition = data["weather"][0]["main"]

    return bot.say(u'%s, %s: %s, %s°, %skmh' % (name, country, condition, temp, windspeed))


@commands('of')
@example('.of London')
def forecast(bot, trigger):
    location = trigger.group(2)

    if not location:
        return bot.say("No location provided.")

    try:
        url = "http://api.openweathermap.org/data/2.5/forecast/daily?units=metric&cnt=3&q=" + location
        response = web.get(url, dont_decode=True)
    except Exception:
        return bot.say("Error while fetching data.")

    data = json.loads(response)
    if data["cod"] != "200":
        if data["message"] == "":
            return bot.say("Error")
        else:
            return bot.say(data["message"])

    name = data["city"]["name"]
    country = data["city"]["country"]

    day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    for item in data["list"]:
        weekday = datetime.fromtimestamp(item["dt"]).weekday()
        minTemp = item["temp"]["min"]
        maxTemp = item["temp"]["max"]
        conditions = item["weather"]["main"]
        windSpeed = item["speed"]

        bot.say(u'%s, %s on %s: min: %s°, max: %s°, %s, %skmh' % (
            name, country, day[weekday], minTemp, maxTemp, conditions, windSpeed))

    return
