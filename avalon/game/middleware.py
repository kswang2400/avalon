from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() and request.path != reverse('login'):
            return HttpResponseRedirect(reverse('login'))

        return