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
    
    secret_codes = SecretCodeDB.objects.all()  # Filter by the current user's secret codes
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
    print(user_name)
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
    print(associate_name)
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
    print(user.username)
    
        # Filter SecretCodeDB objects for the logged-in user and match the user_name field
    matching_codes = SecretCodeDB.objects.filter(user_name__iexact=user.username)  # case-insensitive match
        # Serialize the entire SecretCodeDB object
    serializer = SecretCodeDBSerializer(matching_codes, many=True)
        
        # Return the serialized data (full objects)
    return Response(serializer.data)
    

employee_data = {'1878139': 'Suma Peddinti', '2236674': 'Dasari Chupernechitha', '2240442': 'Rajani Kilari', '2713128': 'Gaddam Saikumar Reddy', '2119279': 'Siva Cheerla', '1856279': 'Suresh Chary Thokanti', '1926456': 'Sivannarayana Penumala', '1286853': 'Debbadi Anusha', '1517126': 'Vinod Naripella', '2553743': 'Sirisha Sirammagari', '1944821': 'Chandramahanti Sai Manasa', '2148333': 'Srinivas Alwala', '1599267': 'Chaitanya Sai Naraharisetti', '2127047': 'Kunta Sumankanth Reddy', '1783107': 'Vikram Pareek', '373064': 'Fazale Sattar Khadernaick', '2288512': 'Vinayak Dilip Pandit', '2762254': 'Hesamuddin Khan', '2688761': 'Bala Prasanna Gorrela', '2314341': 'Borusu Loka Veera Sriram', '567097': 'Srinivasu Medisetti', '2220368': 'Bagari Sravani', '2185462': 'Tushar Shashikant Manjarekar', '2327846': 'Urmila Doddi', '2265988': 'Keerthana Konda', '1951411': 'Nafisa Shaik', '1956031': 'Shivani Alluri', '1240646': 'Srinivasa Rao Polaki', '373463': 'Hafizullah S', '2360058': 'Kothapally Saibabu', '519218': 'Kandikatla Ramya', '1100660': 'Naga Rajeswara Rao Kannikanti', '1952272': 'Karthik Reddy Emireddy', '2128723': 'Abbas Ali Shaik', '2129198': 'Sinduja Singarapu', '2189564': 'Praveena Thumati', '2508958': 'Mallesh Nayak Banavath', '1967326': 'Parimi Bala Guravaiah', '22385941': 'Naveen Garladinne', '2464284': 'Nitin Arun Joshi', '2588768': 'Pooja Rajendra Mahadik', '1768991': 'Naga Durga Sai Ram Kumar Tummuri', '2158826': 'Guna Madhourai', '1623189': 'Sai Ravali Kantamaneni', '554816': 'Kuricheti Keerthana', '1209509': 'Venkatesh Pothuraju', '2650679': 'Reddibathuni Sai Keerthi', '2769612': 'Ketki Diliprao Kulkarni', '1926614': 'Naveen Sai Tanay Ravi', '974634': 'Bhanu Tejaswi Jami', '2129194': 'Haritha Chakali', '2129594': 'Vamsi Krishna Botta', '2390288': 'Pravalika Nimmala', '1780095': 'Sirisha Nagelli', '2574320': 'Appana Satya Venkata Gopala Anil', '2003632': 'Safeena Nasreen', '2539489': 'Sowmya Byatha', '1700529': 'Divya Kalakuntla', '2128564': 'Vamsikrishna Boligerla', '1945314': 'Venkata Vinay Nageswara Rao Mora', '1707240': 'Sravani Sudini', '2168743': 'Venkata Surya Sai Teja Gannavarapu', '2390723': 'Madhuri Telukuntla', '1707532': 'Mohammed Akram Alineik', '2066946': 'Atul Gupta', '1966465': 'Srikanth Thadkapally', '2208397': 'Pavan Sai Anamdasu', '2453308': 'Ravi Kumar Kethuri', '12503686': 'Surya Venkata Naveen Kumar Yerra', '2771934': 'Kumar Kailas Kapoor', '1130277': 'Chandramoulika Boggarapu', '2558996': 'Sai Male', '2562661': 'Sai Dheeraj Behara', '2702074': 'Archana Gadeela', '2774628': 'Harshali Pramod Chaudhari', '2131863': 'Sahilraj Dattatray Karaval', '2463460': 'Pasam Naresh Yadav', '1814728': 'Goli Sai Teja', '2192440': 'Tejaswini Baliboina', '2553922': 'Shivarathri Ravi Kumar', '1947575': 'Peddi Sravani', '2128738': 'Akhil Rajesh Patel Pappula', '2238130': 'Chandra Mounika Kommana', '2009593': 'Sai Manikanta Kothuri', '2276372': 'Sridevi Karri', '2561678': 'Sai Varshith Reddy Benakareddygari', '2560783': 'Aniket Revansiddha Kumbhar', '2810538': 'Srikanth C', '2386770': 'Anusha Chandrala', '2625530': 'Bhargavi Singirikonda', '599586': 'Valluri Papa Prasanna', '2510325': 'Pravalika Lingampalli', '2699194': 'Pemmasani Mounika', '1932279': 'Chandana Jagana', '2584743': 'Nikhil Dakarapu', '2660675': 'Anumolu Dharani', '2240834': 'Bandari Sandeep Kumar', '2341587': 'Roja Meka', '1299203': 'Prajakta Padmakar Shelke', '965935': 'Shivaprakash Kandoori', '1967991': 'Gunturi Venkata Surya Satya Lakshmi', '2175095': 'Atish Ranajit Patil', '2180626': 'Tanvi Hemant Devi', '2199185': 'Mahender Vanga Reddy', '2499539': 'Monica Sharma', '2566861': 'Sanjana Sanjay Pardeshi', '2639927': 'Moulika Guntupalli', '2699392': 'Chiragoni Meenay Kumar', '2650667': 'Varanasi Himabindu', '2592934': 'Akshar Mallik', '345084': 'Sree Bhargavi Vanga', '2003352': 'Bhargavi', '2527248': 'Shaikh Ayyan Shaikh Habib', '2702888': 'Thoom Manideep', '2688599': 'Rajeshwari Vishwakarma', '2649702': 'Battu Manaswini', '2075802': 'Rajavardhan Venkata Mothkuri', '2659805': 'Muddala Saharika', '1646952': 'Neelima Singamaneni', '1584032': 'Kesari Nikhil', '1637782': 'Yaseen Sultana Shaik', '1824403': 'Deepak Chandragoud Nalla', '2133454': 'Anjali Kuncham', '2128965': 'Naveen Savarala', '2129603': 'Pranitha Hanmandla', '2330118': 'Shiva Kumar Uppari', '1238454': 'Hymavathi Areti', '842047': 'Kotagiri Vinoothna', '2128851': 'Lithin Siva Swamy Naidu Majji', '1956254': 'Satya Gaayathri Brahmanapally', '2001959': 'Vamshi Krishna Challa', '2584245': 'Ganji Bhargava Sai', '1771075': 'Venkata Krishna Reddy Dumpa', '1601566': 'Surya Bhaskaram Desalanka', '2235512': 'Vyza Chandrasekhar Reddy', '1720734': 'Pavan Kumar Papolu', '1599881': 'Sabaresh Kumar Ladi'}

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Require token-based authentication
@permission_classes([IsAuthenticated])  # Only allow authenticated users
def update_secret_code(request):
    """Update the secret code record with user_name, isOpened, and openedOn fields"""
    
    user = request.user  # Get the current logged-in user
    
    # Get the 'favNumber' from the request data
    favnumber = request.data.get('favNumber', None)
    print("favnumber"+str(favnumber))
    
    if not favnumber:
        return Response({"error": "Please provide a 'favNumber' in the request body."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find the record by favNumber for the logged-in user
        secret_code = SecretCodeDB.objects.get(fav_number=favnumber)
        
        # Update the record only if the current user hasn't opened it yet
        if secret_code.is_opened:
            return Response({"error": "This record has already been opened by another user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the fields for the authenticated user
        secret_code.user_name = employee_data[user.username]  # Update the user_name with the logged-in user's username
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
                user = User.objects.create_user(username=username, password=password)
                return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            print(user)
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
    print("inside logout")
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
    print("Karthik inside insert")
    app_directory = os.path.dirname(__file__) 
    file_path = os.path.join(app_directory, 'employeedata.json')
    print(file_path)
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