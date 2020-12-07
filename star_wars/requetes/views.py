from django.shortcuts import render
from pymongo import MongoClient
from ssh_pymongo import MongoSession
import csv

session = MongoSession(
    host="devicimongodb028.westeurope.cloudapp.azure.com",
    port=22,
    user='administrateur',
    password='fcwP6h3H',
    uri='mongodb://cloudAdmin:admin@devicimongodb028:30000')
    
db = session.connection['Project']


def user(request):
    ret = []
    requete = db.people.find({"name":"C-3PO"})
    for row in requete:
        ret.append(row)
    tmp = db.people.find_one({"name": "C-3PO"}, {"height": 1, "_id": 0})['height']
    requete = db.people.find({'height':{"$gt":tmp}},{"name":1})
    for row in requete:
        ret.append(row)
    tmp = db.starship.find( {"name": "CR90 corvette"}, {"film":1,"_id":0}).toArray()[0].film
    requete = db.film.find({"_id":{"$in": tmp}},{"title":1})
    for row in requete:
        ret.append(row)
    unwind = {"$unwind":"$films"}
    group = {"$group":{"_id":"$films", "count":{"$sum":1}}}
    match = {"$match":{"_id":3}}
    requete = db.planet.aggregate([unwind,group,match])
    for row in requete:
        ret.append(row)
    context = {}
    context["results"] = ret
    return render(request, 'requetes/user.html', context)

def analyst(request):
    context = {}
    results = []
    with open('requetes\\analyst.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            results.append(row)
    context["results"] = results
    return render(request, 'requetes/analyst.html', context)

def admin(request):
    context = {}
    results = []
    with open('requetes\\admin.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            results.append(row)
    context["results"] = results
    return render(request, 'requetes/admin.html', context)

def home(request):
    return render(request, 'requetes/home.html')