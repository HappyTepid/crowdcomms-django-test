from django.utils import timezone
from .models import UserVisit

class UserVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_visit, _ = UserVisit.objects.get_or_create(user=request.user)
            user_visit.last_seen = timezone.now()
            user_visit.visits += 1
            user_visit.save()
        response = self.get_response(request)
        return response
