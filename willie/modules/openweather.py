# coding=utf8
"""
openweather.py - Willie openweathermap.com module
"""
from __future__ import unicode_literals
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