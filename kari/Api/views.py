from User.models import User, Group
from Contest.models import Contest, ContestProblem
from Problem.models import Problem
from Statistic.models import Board
from Submission.models import Submission
from Api.models import *
from common.utils import make_key
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import zlib
import logging
logger = logging.getLogger('django')

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def userDetail(request, uid):
    try:
        u = User.getById(uid)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = UserSerializer(u)
        return JSONResponse(serializer.data)

def groupDetail(request, gid):
    try:
        g = Group.getById(gid)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = GroupSerializer(g)
        return JSONResponse(serializer.data)

def boardDetail(request, cid):
    try:
        cdata = cache.get(make_key(cid, 'board'))
        if cdata:
            return JSONResponse(eval(zlib.decompress(cdata)))
        c = Contest.getById(cid)
        b = Board()
        b.contest = c
        if request.method == 'GET':
            serializer = BoardSerializer(b)
            data = serializer.data
            cache.set(make_key(cid, 'board'), zlib.compress(str(data)), 60)
            return JSONResponse(data)
    except Exception as e:
        return HttpResponse(e)

def userLogin(request):
    username, password = '', ''
    if request.META.has_key('HTTP_AUTHORIZATION'):
        authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        if authmeth.lower() == 'basic':
            auth = auth.strip().decode('base64')
            username, password = auth.split(':', 1)
    u = User.getUserByRawUsername(username)
    if u!=None and u!=False and u.checkPasswd(password):
        serializer = UserSerializer(u)
        return JSONResponse(serializer.data)
    return HttpResponse(status=404)
