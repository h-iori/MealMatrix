from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('dietplan', views.diet,name='dietplan'),
    path('contact', views.contact,name='contact'),
    path('about', views.about,name='about'),
    path('login', views.userlogin,name='login'),
    path('signup', views.usersignup,name='signup'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('logout', views.loggout,name='logout'),
    path('diet_history/<int:plan_id>', views.diet_history,name='diet_history'),
    
]
