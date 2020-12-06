from django.shortcuts import render
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
import pprint

MONGO_HOST = "devicimongodb028.westeurope.cloudapp.azure.com"
MONGO_DB = "Project"
MONGO_USER = "administrateur"
MONGO_PASS = "fcwP6h3H"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 30000)
)

server.start()

client = MongoClient('devicimongodb028.westeurope.cloudapp.azure.com', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]


def user(request):
    mycol = db["people"]
    obj = mycol.find({'name' : 'C-3PO'}, {'species':1})
    print(mycol)
    j = 0
    for i in mycol:
        print(i)
    context = {}
    results = []  # Put the list of resquest's result to display here
    context["results"] = results
    return render(request, 'requetes/user.html', context)

def analyst(request):
    context = {}
    results = []  # Put the list of resquest's result to display here
    context["results"] = results
    return render(request, 'requetes/analyst.html', context)

def admin(request):
    context = {}
    results = []  # Put the list of resquest's result to display here
    context["results"] = results
    return render(request, 'requetes/admin.html', context)

def home(request):
    context = {}
    results = []  # Put the list of resquest's result to display here
    context["results"] = results
    return render(request, 'requetes/home.html', context)