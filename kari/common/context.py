from User.models import User

def user(request):
    u = User.getSessionUser(request.session)
    if u!=None and u!=False:
        return {'user':u}
    else:
        return {'user':None}
