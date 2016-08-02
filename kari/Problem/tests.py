"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.management.base import NoArgsCommand
from django.conf import settings
from Problem.models import *

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        p = Problem.getById(2)
        try:
            p.copyProblemFromID(54)
            print p
        except:
            print 'Error'

