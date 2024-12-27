from django.urls import path
from .views import event_list,event_detail,get_highlights_list, get_important_person_list

urlpatterns = [
    path('get-highlights/', get_highlights_list, name='get-highlights'),
    path('get-important-persons/', get_important_person_list, name='get-important-persons'),
    path('get-events/', event_list, name='get-events'),
    path('get-event-detail/<int:pk>', event_detail, name='get-event-detail'),

]


