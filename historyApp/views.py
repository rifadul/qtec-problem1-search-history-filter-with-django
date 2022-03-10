from django.shortcuts import render
from django.http import HttpResponse
from .models import SearchHistory
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date,timedelta
from django.core import serializers


# Create your views here.
def HomeView(request):
    template_name = 'index.html'
    context = {}
    data = SearchHistory.objects.all().values('keyword').order_by('keyword').annotate(the_count=Count('keyword'))
    user = User.objects.all()
    context['data'] = data
    context['user'] = user
    return render(request,template_name,context)


@csrf_exempt
def filter_history_results(request):
    if request.method == 'POST':
        # <===========================  get the data =========================== >
        data = json.loads(request.body)

        # <=========================== declare the all variable =========================== >
        keywords = data['keyword']
        users = data['user']
        itemsDate = data['date']
        result = []
        today = date.today()
        yesterday = today - timedelta(days = 1)
        last_week= today - timedelta(days=7)
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)

#  <===========================  In this function format the date in YYYY-MM-DD format =========================== >
        def formatTheDate(dayName):
            if(dayName=='today'):
                    return today.strftime("%Y-%m-%d")
            elif(dayName=='yesterday'):
                    return yesterday.strftime("%Y-%m-%d")
                    
            elif(dayName=='last_week'):
                    return last_week.strftime("%B %d,%Y")
                    
            elif(dayName=='lastMonth'):
                    return lastMonth.strftime("%B %d,%Y")


# <=========================== All filter operations start with json data =================================>
        
        # <===========================  only keyword base data filter ===========================>
        if(keywords !=[] and users ==[] and itemsDate==[]):
            for keyword in keywords:
                result += list(SearchHistory.objects.filter(keyword__icontains=keyword))

        # <=========================== only users base data filter ===========================>
        elif(users !=[] and keywords ==[] and itemsDate==[]):
            for user in users:
                    result += list(SearchHistory.objects.filter(user__username=user))
        
        # <=========================== only Date base data filter ===========================>
        elif(itemsDate !=[] and users ==[] and keywords ==[]):
            for itemDate in itemsDate:
                result += list(SearchHistory.objects.filter(date__icontains=formatTheDate(itemDate)))

        # <=========================== only user and keyword base data filter ===========================>
        elif(keywords !=[] and users !=[] and itemsDate==[]):
            for user in users:
                for keyword in keywords:
                    print('d',keyword)
                    result += list(SearchHistory.objects.filter(user__username=user,keyword__icontains=keyword))


        # <=========================== only user and Date base data filter ===========================>
        elif(itemsDate!=[] and users !=[] and keywords ==[]):
            for user in users:
                for itemDate in itemsDate:
                    result += list(SearchHistory.objects.filter(user__username=user,date__icontains=formatTheDate(itemDate)))

        # <=========================== only Keyword and Date base data filter ===========================>
        elif(itemsDate!=[] and keywords !=[] and users ==[]):
            for keyword in keywords:
                for itemDate in itemsDate:
                    result += list(SearchHistory.objects.filter(keyword__icontains=keyword,date__icontains=formatTheDate(itemDate)))
                

        # <=========================== user and keyword and date base data filter  ===========================>       
        elif(keywords !=[] and users !=[]and itemsDate!=[]):
            for user in users:
                for keyword in keywords:
                    for itemDate in itemsDate:
                        print('d',itemDate)
                        result += list(SearchHistory.objects.filter(user__username=user,keyword__icontains=keyword,date__icontains=formatTheDate(itemDate)))
    
        # <=========================== return json respons ===========================>
        qs_json = serializers.serialize('json', result)
        return HttpResponse(qs_json, content_type='application/json')