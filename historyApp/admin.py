from django.contrib import admin
from .models import SearchHistory

# Register your models here.
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    '''Admin View for SearchHistory'''

    list_display = ['id','user','keyword','date','time']