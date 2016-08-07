# coding: utf-8
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from Cheat.models import Cheat
from django.shortcuts import render_to_response, render, redirect
from kari.const import Const

def index(request):
    return render(request, Const.ERROR_PAGE, {'errmsg': 'asdgb', })
	#return render_to_response("newtpl/Cheat/antiCheat.html")	
	#return render_to_response("newtpl/Cheat/antiCheat.html")	
	#return render_to_response("Submission/Submit.html")
def addRecord(request):
	try:
		contestid = request.GET.get('contestid','-1')
		if contestid=='':
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		Cheat.addRecord(contestid)
		return render_to_response("Cheat/addComplete.html")
	except Exception as e:
		return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
		#return render( request, 'error.html','errmsg'=str(e))
#def goBack(request):
#	return render_to_response("Cheat/antiCheat.html")

def showResult(request):
	try:
		cheat_list = Cheat.getCheatList()
		cheat_user_list = []
		for cl in cheat_list:
			cheat_user = []
			cheat_user.append(cl.user1)
			cheat_user.append(cl.user2)
			cheat_user.append(cl.contest_problem)
			cheat_user.append(cl.ratio)
			cheat_user_list.append(cheat_user)

		return render_to_response("Cheat/showResult.html", {'cheat_list':cheat_user_list})
	except Exception as e:
		return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
		#return render( request, 'error.html','errmsg'=str(e))

#def getGroupByUser():
#	MAX_USER = 2000
#	father = {}	
#	user_to_pos = {}
#	cnt = 0
#	cheat_list = Cheat.getCheatList()
#	for cl in cheat_list:
#		user1 = cl.user1
#		user2 = cl.user2
#		fx = father.get(user1, 0)
#		if fx=0:
#			father[user1] = user1
#		fy = father.get(user2, 0)
#		if fy=0:
#			father[user2] = user2
#		fx = user1
#		while fx!=father[fx]:
#			fx = father[fx]
#		root = fx
#		fx = user1
#		while fx!=root:
#			temp = father[fx]
#			father[fx] = root
#			fx = temp
#		fx = root
#		fy = user2
#		while fy!=father[fy]:
#			fy = father[fy]
#		root = fy
#		fy = user2
#		while fy!=root:
#			temp = father[fy]
#			father[fy] = root
#			fy = temp
#		fy = root
#		if fx!=fy:
#			father[fx] = fy
#		
#	cheat_user_list = []
#	for i in range(MAX_USER):
#		cheat_user_list.append([])
#	for cl in cheat_list:
#		fx = user1
#		while fx!=father[fx]:
#			fx = father[fx]
#		if user_to_pos.get(fx, -1)=-1:
#			user_to_pos[fx] = cnt++
#		cheat_user_list[user_to_pos.get(fx,-1)].append(user1)
#		fy = user2
#		while fy!=father[fy]:
#			fy = father[fy]
#		if user_to_pos.get(fy, -1)=-1:
#			user_to_pos[fy] = cnt++
#		cheat_user_list[user_to_pos.get(fy,-1)].append(user2)
#
#
