"""apquiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('save/', views.save,name='save'), # <-- added
    path('login/', LoginView.as_view(redirect_field_name='controller/dashboard.html',template_name="controller/login.html")),
    path('dashboard/',views.dashboard),
    path('addTest/',views.addTest),
    path('saveTest/',views.saveTest),
    path('logout/',views.logout),
    path('addQuestion/',views.addQuestion),
    path('saveQuestion/',views.saveQuestion),
    path('viewTest/<int:id>',views.viewTest),
    path('viewTests',views.viewTests),
    path('viewStudents',views.viewStudents),
    path('viewStudent/<int:id>',views.viewStudent),
    path('viewTeachers',views.viewTeachers),
    path('viewTeacher/<int:id>',views.viewTeacher),
    path('pending/<int:id>',views.pending),
    path('saveStudent/',views.saveStudent),
    path('addStudent/',views.addStudent),
    path('addTeacher',views.addTeacher),
    path('saveTeacher',views.saveTeacher)
    
]

