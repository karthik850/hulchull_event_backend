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

from datetime import datetime

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