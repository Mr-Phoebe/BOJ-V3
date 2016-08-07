from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator

from common.err import Err

from User.models import *

def submit(request):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, err='not login')
        return render(request, 'newtpl/print/submit.html', {'uname': str(u), 'tpl': {'sp': True}}) 
    except Exception as e:
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e), }, )
