"""SailingManager URL Configuration

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
from django.contrib import admin
from django.urls import path
from SailingRaceManager.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPage.as_view()),

    path('manage/', OodHomeView.as_view()),
    path('manage/run/<pk>', RunRaceView.as_view()),

    path('ajax/addLap/', AjaxAddLap.as_view()),
    path('ajax/changeStatus/', AjaxChangeStatus.as_view()),
    path('ajax/results/<pk>', AjaxGetResults.as_view()),

    path('boats/', BoatListView.as_view()),
    path('boats/edit/<pk>', BoatEditFormView.as_view()),
    path('boats/new', BoatNewFormView.as_view()),
    path('boats/delete/<pk>', BoatDeleteView.as_view()),

    path('racers/', RacerListView.as_view()),
    path('racers/edit/<pk>', RacerEditFormView.as_view()),
    path('racers/new', RacerNewFormView.as_view()),
    path('racers/delete/<pk>', RacerDeleteView.as_view()),

    path('race/edit/<pk>', RaceEditFormView.as_view()),
    path('race/new', RaceNewFormView.as_view()),
    path('race/delete/<pk>', RaceDeleteView.as_view()),

    path('results/', ResultsHomeView.as_view()),
    path('results/<pk>', RaceResultsView.as_view()),

]
