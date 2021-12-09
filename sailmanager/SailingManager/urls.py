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
from django.urls import path, re_path
from SailingRaceManager.views import *
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPage.as_view(),name="home"),
    re_path(r'^accounts/login/$', login, {'template_name': 'admin/login.html'}),
    re_path(r'^accounts/logout/$', logout),

    path('manage/', OodHomeView.as_view(), name="manage"),
    path('manage/run/<pk>', RunRaceView.as_view(), name="manageRace"),

    path('ajax/addLap/', AjaxAddLap.as_view(),name="addLap"),
    path('ajax/changeStatus/', AjaxChangeStatus.as_view(),name="changeStatus"),
    path('ajax/results/<pk>', AjaxGetResults.as_view(),name="results"),
    path('ajax/setStartTime/<pk>', AjaxSetRaceStart.as_view(),name="results"),

    path('boats/', BoatListView.as_view(),name="boatList"),
    path('boats/edit/<pk>', BoatEditFormView.as_view(),name="boatEdit"),
    path('boats/new', BoatNewFormView.as_view(),name="boatNew"),
    path('boats/delete/<pk>', BoatDeleteView.as_view(),name="boatDelete"),
    path('boats/upload', UploadBoatList.as_view(),name="boatUpload"),

    path('racers/', RacerListView.as_view(),name="racerList"),
    path('racers/edit/<pk>', RacerEditFormView.as_view(),name="racerEdit"),
    path('racers/new', RacerNewFormView.as_view(),name="racerNew"),
    path('racers/new_official', OfficialNewFormView.as_view(),name="racerNewOfficial"),
    path('racers/delete/<pk>', RacerDeleteView.as_view(),name="racerDelete"),

    path('race/edit/<pk>', RaceEditFormView.as_view(),name="raceEdit"),
    path('race/new', RaceNewFormView.as_view(),name="raceNew"),
    path('race/delete/<pk>', RaceDeleteView.as_view(),name="raceDelete"),

    path('results/', ResultsHomeView.as_view(), name="results"),
    path('results/<pk>', RaceResultsView.as_view(), name="resultsRace"),
    path('results/detailed/<pk>', RaceResultsDetailedView.as_view(), name="resultsRaceDetailed"),

]
