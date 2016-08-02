#!/usr/bin/env python
# coding: utf-8
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kari.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
