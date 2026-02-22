from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('home', views.index, name = 'home'),
    path('logout', views.logoutPage, name='logout'),
    path('login', views.loginPage, name='login'),    # URL for login page
    path('signup/', views.signUpPage, name='signup'),  # URL for signup page
    path('dashboard',views.dashboard, name= 'dashboard'),
    path('results/<str:sub_topic>/', views.results, name='results'),
    path('page1/', views.page1, name='page1'),
    path('analysis',views.analysis,name='analysis'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
