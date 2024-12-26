from django.urls import path
from .views import create_user, admin_secretcode_list, get_my_secret_code, logout_view, search_by_associate_name, search_by_user_name, update_secret_code, user_secretcode_list, login_view

urlpatterns = [
    path('admin/secretcodes/', admin_secretcode_list, name='admin-secretcode-list'),
    path('user/secretcodes/', user_secretcode_list, name='user-secretcode-list'),
    path('create-user/', create_user, name='create-user'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search-by-username/', search_by_user_name, name='search-by-username'),  # New URL for search
    path('search_by_associate_name/',search_by_associate_name,name='search_by_associate_name'),
    path('get-my-secret-code/',get_my_secret_code,name='get_my_secret_code'),
    path('update-secret-code/', update_secret_code, name='update-secret-code'),
]
