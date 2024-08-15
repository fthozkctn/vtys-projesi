"""
URL configuration for proje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from projeekle import views
from projeekle.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index,name = "index"),
    path('user/', include("user.urls")),
    path('projeler/',views.projeler,name = "projeler"),
    path('proje_ekle/',views.projeEkle,name = "proje_ekle"),
    path('projeler/<int:id>', views.detail, name="detail"),
    path('user/gorevlerim/<int:id>', views.taskDetail, name="görevlerim"),
    path('projeler/update/<int:id>', views.updateProje, name = "update"),
    path('projeler/update/<int:id>/create_task/', views.createTask, name = 'create_task'),
    path('projeler/delete/<int:id>', views.deleteProje, name = 'delete'),
    path('userlist/<int:id>', views.userDetail,  name="userdetail"),
    path('user/gorevlerim/<int:id>/submit', views.submitTask, name="submittask"),
    path('projeler/<int:id>/task', views.taskDetailProje, name="taskdetail"),
]
