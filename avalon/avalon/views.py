from django.http import HttpResponse

def profile(request):
    inline_template = """
        user: {user}<br>
        date_joined: {date_joined}<br>
        last_login: {last_login}<br>
    """.format(
            user=request.user.username,
            date_joined=request.user.date_joined,
            last_login=request.user.last_login,
        )
    return HttpResponse(inline_template)