from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

class AuthRequiredMiddleware(object):
    def process_request(self, request):
        unauthenticated_views = [
            reverse('login'),
            reverse('signup'),
        ]

        if not request.user.is_authenticated() and request.path not in unauthenticated_views:
            return HttpResponseRedirect(reverse('login'))

        return