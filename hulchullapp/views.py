from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import SecretCodeDB
from .serializers import SecretCodeDBSerializer, SecretCodeUserSerializer, UserCreationSerializer, LoginSerializer

from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.http import JsonResponse
from datetime import datetime
import json


names_list = ['Kiran pedamallu','laxman akella', 'Rajesh reddy','Nantha Kumar Selvaraj', 'ramya radhakrishna','geetha vemula','gowtham shanmugam','vijay balchander','koty manoraj','rachana rayala','manasa bondada','sai krishna majji','chandu chittibomma','mukhram khan','manish Anand','santosh julakanti','deepak chandra goud','lithin siva swamy naidu', 'Chandra Sekhar Reddy Mukkarapu'
    'Kuricheti Keerthana', 'Bhanu Tejaswi Jami', 'Divya Kalakuntla', 'Safeena Nasreen', 'Pravalika Nimmala', 'Sravani Sudini', 'Venkatesh Pothuraju', 'Karthik Reddy Emireddy', 'Vamsikrishna Boligerla', 'Naveen Sai Tanay Ravi', 'Naveen Garla dinne', 'Praveena Thumati', 'Sal Ravall Kantamaneni', 'Vamsi Krishna Botta', 'Sirisha Nagelli', 'Abbas Ali Shaik', 'Venkata Vinay Nageswara Rao Mora', 'Sinduja Singarapu', 'SriDevi Karri', 'Srinivas Polaki', 'Parimi Bala Guravaiah', 'Sabaresh Kumar Ladi', 'Madhuri Telukuntla', 'Haritha Chakali', 'Vamshi Krishna Challa', 'Kotagiri Vinoothna', 'Anjali Kuncham', 'Naveen Savarala', 'Shiva Kumar Uppari', 'Satya Gaayathri Brahmanapally', 'Hymavathi Areti', 'Akhil Rajesh Patel Pappula', 'Peddi Sravani', 'Mohammed Akram Alinelk', 'Srikanth Thadkapally', 'Sivannarayana Penumala', 'Srinivasu Medisetti', 'Rajani Kilari', 'Shivani Alluri', 'Nafisa Shaik', 'Vikram Pareek', 'Siva Cheerla', 'Borusu Loka Veera Sriram', 'Chandramoulika Boggarapu', 'Surya Venkata Naveen Kumar Yerra', 'Sree Bhargavi Vanga', 'Praveen Kumar', 'Shivaprakash Kandoorl', 'Kesari Nikhil', 'Bandari Sandeep Kumar', 'Anusha Chandrala', 'Valluri Papa Prasanna', 'Prajakta Padmakar Shelke', 'Iragala Bhargavi', 'Chandana Jagana', 'Archana Gadeela', 'Chiragoni Meenay Kumar', 'Rajeshwari Vishwakarma', 'Thoom Manideep', 'Ganji Bhargava Sai', 'Gunturi Venkata Surya Satya Lakshmi', 'Bhargavi Singirikonda', 'Yaseen Sultana Shaik', 'Anumolu Dharani', 'Vinod Naripella', 'Kunta Sumankanth Reddy', 'Kandikatla Ramya', 'Hesamuddin Khan', 'Urmila Doddi', 'Suresh Chary Thokanti', 'Bagari Sravani', 'Suma Peddinti', 'Pranitha Hanmandla', 'Dasari Chupernechitha', 'Keerthana Konda', 'Bala Prasanna Gorrela', 'Chandramahanti Sai Manasa', 'Pavan Sai Anamdasu', 'Srinivas Alwala', 'Debbadi Anusha', 'Sirisha Sirammagari', 'Gaddam Saikumar Reddy', 'Ravi Kumar Kethurl', 'Sowmya Byatha', 'Saj Male', 'Shivarathri Ravi Kumar', 'Neelima Singamaneni', 'Mahender Vanga Reddy', 'Muddala Saharika', 'Shaikh Ayyan Shaikh Habib', 'Kothapally Saibabu', 'Rajavardhan Venkata Mothkuri', 'Battu Manaswini', 'Varanasi Himabindu', 'Nikhil Dakarapu', 'Pravalika Lingampalli', 'Roja Meka', 'Chandra Mounika Kommana', 'Sai Manikanta Kothuri', 'Prashanth Kumar Goud Kurella', 'Tharun Teja Akula', 'Chaitanya Sai Naraharisetti', 'Sai Varshith Reddy Benakareddygari', 'Mallesh Nayak Banavath', 'Naga Durga Sai Ram Kumar Tummuri', 'Reddibathuni Sai Keerthi', 'Srikanth Chinta', 'Venkata Surya Sai Teja Gannavarapu', 'Sanja Mehroze', 'Appana Satya Venkata Gopala Anil', 'Prathyusha Murari', 'Pasam Naresh Yadav', 'Goli Sai Teja', 'Sai Dheeraj Behara', 'Tejaswini Baliboina']


import Levenshtein

def calculate_matching_percentage(name1, name2):
    # Calculate the Levenshtein distance
    distance = Levenshtein.distance(name1.lower(), name2.lower())
    
    # Find the length of the longest string
    max_len = max(len(name1), len(name2))
    
    # Calculate the matching percentage
    matching_percentage = ((max_len - distance) / max_len) * 100
    return matching_percentage

def get_max_matching_name(reference_name, names_list):
    max_percentage = 0
    best_match = ""
    
    for name in names_list:
        percentage = calculate_matching_percentage(reference_name, name)
        if percentage > max_percentage:
            max_percentage = percentage
            best_match = name
    
    return best_match, max_percentage



@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAdminUser])  # Only allow admin users
def admin_secretcode_list(request):
    """Admin can view all secret codes including the usernames"""
    secret_codes = SecretCodeDB.objects.all()
    serializer = SecretCodeDBSerializer(secret_codes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAuthenticated])  # Any authenticated user can access
def user_secretcode_list(request):
    user= request.user
    # key = employee_data[str(user.username)]
    secret_codes = SecretCodeDB.objects.exclude(associate_name__iexact = user.username)  # Filter by the current user's secret codes
    serializer = SecretCodeUserSerializer(secret_codes, many=True)

    # Exclude the username from the response for users
     # Remove the username field

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAdminUser])  # Only allow authenticated users
def search_by_user_name(request):
    """Search for secret codes where user_name matches the query parameter"""
    
    # Get the 'user_name' query parameter
    user_name = request.query_params.get('user_name', None)
    #user_name = request.data.get('user_name', None)

    if user_name:
        # Filter SecretCodeDB objects for the logged-in user and match the user_name field
        matching_codes = SecretCodeDB.objects.filter(user_name=user_name)  # case-insensitive match
        # Serialize the entire SecretCodeDB object
        serializer = SecretCodeDBSerializer(matching_codes, many=True)
        
        # Return the serialized data (full objects)
        return Response(serializer.data)
    else:
        # If no 'user_name' is provided in the query, return an error
        return Response({"error": "Please provide a 'user_name' query parameter."}, status=400)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAdminUser])  # Only allow authenticated users
def search_by_associate_name(request):
    """Search for secret codes where user_name matches the query parameter"""
    
    # Get the 'user_name' query parameter
    associate_name = request.query_params.get('associate_name', None)
    #user_name = request.data.get('user_name', None)
    if associate_name:
        # Filter SecretCodeDB objects for the logged-in user and match the user_name field
        matching_codes = SecretCodeDB.objects.filter(associate_name__iexact=associate_name)  # case-insensitive match
        # Serialize the entire SecretCodeDB object
        serializer = SecretCodeDBSerializer(matching_codes, many=True)
        
        # Return the serialized data (full objects)
        return Response(serializer.data)
    else:
        # If no 'user_name' is provided in the query, return an error
        return Response({"error": "Please provide a 'user_name' query parameter."}, status=400)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAuthenticated])  # Only allow authenticated users
def get_my_secret_code(request):
    """Search for secret codes for the logged-in user where user_name matches the query parameter"""
    
    user = request.user  # Get the current logged-in user
    # key = employee_data[str(user.username)]

        # Filter SecretCodeDB objects for the logged-in user and match the user_name field
    matching_codes = SecretCodeDB.objects.filter(user_name__iexact=user.username)  # case-insensitive match
        # Serialize the entire SecretCodeDB object
    serializer = SecretCodeDBSerializer(matching_codes, many=True)
        
        # Return the serialized data (full objects)
    return Response(serializer.data)
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAuthenticated])  # Only allow authenticated users
def update_secret_code(request):
    """Update the secret code record with user_name, isOpened, and openedOn fields"""
    
    user = request.user  # Get the current logged-in user
    
    # Get the 'favNumber' from the request data
    favnumber = request.data.get('favNumber', None)
    
    if not favnumber:
        return Response({"error": "Please provide a 'favNumber' in the request body."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find the record by favNumber for the logged-in user
        secret_code = SecretCodeDB.objects.get(fav_number=favnumber)
        
        # Update the record only if the current user hasn't opened it yet
        if secret_code.is_opened:
            return Response({"error": "This record has already been opened by another user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the fields for the authenticated user
        secret_code.user_name = user.username  # Update the user_name with the logged-in user's username
        secret_code.is_opened = True  # Set isOpened to True
        secret_code.opened_on = datetime.now()  # Set the openedOn field to the current timestamp
        
        secret_code.save()  # Save the updated record
        
        # Return the updated secret code record as response
        serializer = SecretCodeDBSerializer(secret_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except SecretCodeDB.DoesNotExist:
        return Response({"error": "Record with the provided favNumber does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to create a new user
def create_user(request):
    """Create a new user with username and password"""
    if request.method == 'POST':
        # Deserialize incoming data
        serializer = UserCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Create the user and set the password
            try:
                best_match, max_percentage = get_max_matching_name(username, names_list)
                user = User.objects.create_user(username=best_match, password=password)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key,"username":user.username,"isadmin":user.is_staff}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except KeyError as e:
                return Response({"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except IntegrityError as e:
                return Response(
                        {"error": "A user with this username already exists."},
                        status=status.HTTP_409_CONFLICT  # Use 409 Conflict for "already exists"
                        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to log in
def login_view(request):
    """Login view to authenticate a user and provide a token"""
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            best_match, max_percentage = get_max_matching_name(username, names_list)
            # Authenticate the user
            user = authenticate(username=best_match, password=password)
            if user is not None:
                # Generate or retrieve token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key,"username":user.username,"isadmin":user.is_staff}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logs out the user by deleting their authentication token."""
    
    try:
        # Get the token associated with the current user
        token = Token.objects.get(user=request.user)
        # Delete the token to log the user out
        token.delete()
        
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
    except Token.DoesNotExist:
        return Response({"message": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)



from django.conf import settings
import os

@api_view(['POST'])
@permission_classes([AllowAny])
def insert_bulk_data(request):
    data=[]
    app_directory = os.path.dirname(__file__) 
    file_path = os.path.join(app_directory, 'employeedata.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    bulk_instances = []
    for entry in data:
        bulk_instances.append(
            SecretCodeDB(
                fav_number=entry["fav_number"],
                associate_name=entry["associate_name"],
                gender=entry["gender"]
            )
        )

    # Perform the bulk create operation
    SecretCodeDB.objects.bulk_create(bulk_instances)

    return JsonResponse({"message": "Data inserted successfully!"})