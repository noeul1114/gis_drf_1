from django.http import HttpResponseForbidden

from profileapp.models import Profile


def profile_ownership_required(func):
    def decorated(request, *args, **kwargs):
        target_profile = Profile.objects.get(kwargs['pk'])
        if not target_profile.owner == request.user:
            return HttpResponseForbidden()
        else:
            return func(request, *args, **kwargs)
    return decorated
