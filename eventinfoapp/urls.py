from django.urls import path
from .views import event_list,event_detail, get_all_events, get_all_teams, get_event_details,get_highlights_list, get_important_person_list, get_team_details, update_event_team_scores

urlpatterns = [
    path('get-highlights/', get_highlights_list, name='get-highlights'),
    path('get-important-persons/', get_important_person_list, name='get-important-persons'),
    path('get-events/', event_list, name='get-events'),
    path('get-event-detail/<int:pk>', event_detail, name='get-event-detail'),
    path('teams/<int:team_id>/', get_team_details, name='get_team_details'),
    path('teams/', get_all_teams, name='get_all_teams'),
    path('events/<int:event_id>/', get_event_details, name='get_event_details'),
    path('events/', get_all_events, name='get_all_events'),
    path('events/<int:event_id>/update-scores/', update_event_team_scores, name='update_event_team_scores'),
]


