# coding: utf-8
#from django.core.management import setup_environ
#from django.conf import settings
#settings.configure()

from Register.models import *
f = open("/home/buptacm/oj/kari/bronze.txt", "r")
count = 0
for name in f:
    name = name.rstrip('\n')
    #print name
    team = Team.getByName(name)
    print team.name
    team.status = 'Bronze'
    team.save()
    count += 1

print count
