from django.urls import path
from webapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    # path('login/', views.loginView, name="login"),
    # path('logout/', views.logoutView, name="logout"),
    path('profile/<str:id>/', views.profile, name="profile"),
    path('add_post/', views.add_post, name="add_post"),
    path('edit_post/<str:id>/', views.edit_post, name="edit_post"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),


    path('login/', auth_views.LoginView.as_view(
        template_name='login.html', redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    path('about/', views.about, name="about"),
]