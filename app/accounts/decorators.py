from django.shortcuts import redirect


def is_unauth(func):
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect("home")

    return decorator


def is_auth(func):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect("home")

    return decorator
