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
    obj = db.people.find( {'name' : 'C-3PO'}, {'species':1} )
    return render(request, 'requetes/user.html')

def analyst(request):
    return render(request, 'requetes/analyst.html')

def admin(request):
    return render(request, 'requetes/admin.html')

def home(request):
    return render(request, 'requetes/home.html')