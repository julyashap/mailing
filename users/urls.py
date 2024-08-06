from django.urls import path
from users.apps import UsersConfig
from users.views import RegistrationView, email_confirm, LoginView, LogoutView, UserListView, user_blocking, \
    user_unblocking, UserDetailView, UserUpdateView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_confirm, name='email_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('change/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),


    path('', UserListView.as_view(), name='user_list'),
    path('user-block/<int:pk>/', user_blocking, name='user_block'),
    path('user-unblock/<int:pk>/', user_unblocking, name='user_unblock'),
]
