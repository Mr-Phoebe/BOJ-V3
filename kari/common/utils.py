from django.utils.http import is_safe_url

def referer(request):
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
        if not is_safe_url(url, request.get_host()):
            url = '/'
    else:
        url = '/'
    return url

def queryString(**kwargs):
    return '?'+'&'.join(["%s=%s" % (k, v) for k, v in kwargs.items()])

def make_key(key_prefix, key):
    return ':'.join((key_prefix, key))
