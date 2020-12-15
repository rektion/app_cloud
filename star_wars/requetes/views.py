from django.shortcuts import render
from pymongo import MongoClient
from ssh_pymongo import MongoSession
from .forms import ChoiceForm

session = MongoSession(
    host="devicimongodb028.westeurope.cloudapp.azure.com",
    port=22,
    user='administrateur',
    password='fcwP6h3H',
    uri='mongodb://cloudAdmin:admin@devicimongodb028:30000')
    
db = session.connection['Project']


def user(request):
    ret = []
    tempo = []
    
    #------------------#
    requete = db.people.find({"name":"C-3PO"})
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []
    
    #------------------#
    tmp = db.people.find_one({"name": "C-3PO"}, {"height": 1, "_id": 0})['height']
    requete = db.people.find({'height':{"$gt":tmp}},{"name":1})
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []  
    
    #------------------#  
    tmp = (db.starship.find( {"name": "CR90 corvette"}, {"film":1,"_id":0})[0])['film']
    requete = db.film.find({"_id":{"$in": tmp}},{"title":1})
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []
    
    #------------------#
    unwind = {"$unwind":"$films"}
    group = {"$group":{"_id":"$films", "count":{"$sum":1}}}
    match = {"$match":{"_id":3}}
    requete = db.planet.aggregate([unwind,group,match])
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    context = {}
    context["results"] = ret
    return render(request, 'requetes/user.html', context)

def analyst(request):
    context = {}
    ret = []
    tempo = []
    
    #------------------#
    requete = db.planet.find({"people.films":{"$size":6}},{"name":1})
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []

    #------------------#
    mean= {"$group" :{"_id":'$species',"avgSize":{"$avg":'$height'}}}
    sort = {"$sort" : {"avgSize":-1}}
    limit = {"$limit":1}
    species_max = (list(db.people.aggregate([mean,sort,limit]))[0])['_id']
    match= {"$match":{'species':species_max}}
    unwind = {"$unwind": '$starships'}
    group= {"$group" :{"_id": '$starships', "count" : {"$sum":1}}}
    requete = db.people.aggregate([match,unwind,sort,limit]) # Cette requete ne retourne rien, est-ce normal ?
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []

    #------------------#
    group ={"$group":{"_id":'$species', "avgSize":{"$avg":'$height'},"stdSize":{"$stdDevSamp":'$height'}, "peoples":{"$push":'$$ROOT'}}}
    project1= {"$project" :{"sum":{"$sum":['$avgSize','$stdSize']},"peoples":1}}
    unwind={"$unwind":'$peoples'}
    project2= {"$project" :{"sum": 1, "height" :'$peoples.height',"starships" :'$peoples.starships'}}
    match={"$match":{"$expr":{"$gt":['$height', '$sum']}}}
    unwind2={"$unwind":'$starships'}
    project3={"$project":{"starships":"$starships.class","_id":0}}
    requete = db.people.aggregate([group,project1, unwind, project2,match,unwind2,project3])
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []

    #------------------#
    project={"$project": { "count": { "$size":"$starships" },"homeworld":"$homeworld"}}
    sort={"$sort":{"count":-1}}
    homeworld_id_tmp = list(db.people.aggregate([project,sort]))[0]["homeworld"]
    """
    homeworld_id = []
    for element in homeworld_id_tmp:
        homeworld_id.append(element['homeworld'])
    """
    requete = db.people.find({"homeworld":homeworld_id_tmp},{"name":1})
    for row in requete:
        tempo.append(row)
    ret.append(tempo)
    tempo = []
    context["results"] = ret
    return render(request, 'requetes/analyst.html', context)

def admin(request):
    form = ChoiceForm()
    context = {}

    db2 = session.connection['config']
    test = db2.shards

    if request.POST:
        if form.is_valid():
            print("on est al")
            pass
    else:
        context['form'] = form

    return render(request, 'requetes/admin.html', context)
    

def home(request):
    return render(request, 'requetes/home.html')