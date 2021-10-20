from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserVisit

class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        now = timezone.now()

        all_visitors = UserVisit.objects.count()
        recent_visitors = UserVisit.objects.filter(last_seen__gte=now-timedelta(hours=1)).count()
        all_visits = UserVisit.objects.aggregate(Sum('visits'))['visits__sum']

        data = {
            'version': 1.0,
            'time': timezone.now(),
            'recent_visitors': recent_visitors,
            'all_visitors': all_visitors,
            'all_visits': all_visits,
        }
        return Response(data)

