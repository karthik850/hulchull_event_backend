from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import EventImages, Events,Highlights,ImportantPersons, Teams
from .serializers import EventImagesSerializer, EventSerializer, HighlightsSerializer,ImportantPersonsSerializer, TeamSerializer
from django.shortcuts import get_object_or_404


# Create your views here.

# List all events or create a new Events
@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def event_list(request):
    if request.method == 'GET':
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete an Events by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def event_detail(request, pk):
    try:
        Events = Events.objects.get(pk=pk)
    except Events.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(Events)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(Events, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Events.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_highlights_list(request):
    if request.method == 'GET':
        highlights = Highlights.objects.all()
        serializer = HighlightsSerializer(highlights, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_important_person_list(request):
    if request.method == 'GET':
        importantPersons = ImportantPersons.objects.all()
        serializer = ImportantPersonsSerializer(importantPersons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImportantPersonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_team_details(request, team_id):
    """Functional view to get team details by ID."""
    team = get_object_or_404(Teams, id=team_id)
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_teams(request):
    """View to get all team information."""
    teams = Teams.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_details(request, event_id):
    """Functional view to get event details by ID."""
    event = get_object_or_404(Events, id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_events(request):
    """View to get all event information."""
    events = Events.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_event_images(request):
    """View to get all event information."""
    eventImages = EventImages.objects.all()
    serializer = EventImagesSerializer(eventImages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_event_team_scores(request, event_id):
    """Update team scores for a specific event, ensuring to handle position changes."""
    event = get_object_or_404(Events, id=event_id)

    # Get the previous spots before the update
    previous_spots = {
        'team_spot_1': event.team_spot_1,
        'team_spot_2': event.team_spot_2,
        'team_spot_3': event.team_spot_3,
        'team_spot_4': event.team_spot_4,
        'team_spot_5': event.team_spot_5,
    }

    # Update the team spots based on the request data
    team_spots_data = request.data  # Assuming the request data contains the new team spots

    event.team_spot_1 = team_spots_data.get('team_spot_1', event.team_spot_1)
    event.team_spot_2 = team_spots_data.get('team_spot_2', event.team_spot_2)
    event.team_spot_3 = team_spots_data.get('team_spot_3', event.team_spot_3)
    event.team_spot_4 = team_spots_data.get('team_spot_4', event.team_spot_4)
    event.team_spot_5 = team_spots_data.get('team_spot_5', event.team_spot_5)

    event.save()  # This will trigger score updates based on position changes

