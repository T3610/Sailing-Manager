from django.views.generic import ListView, TemplateView, FormView, View, UpdateView
from django.views.generic.edit import DeleteView
from SailingRaceManager.models import Boat, Race, Racer, RaceEvent
from SailingRaceManager.forms import BoatForm, RacerForm, RaceForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .serializers import RaceEventSerializer
from django.db.models import DurationField, ExpressionWrapper, Q, F, Subquery
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime
from django.utils import timezone
# Create your views here.

class IndexPage(TemplateView):
    template_name = 'index.html'


# Boat management classes
class BoatListView(ListView):
    model = Boat
    template_name="boat/boat_list.html"

class BoatEditFormView(FormView):
    template_name = 'boat/boat_form.html'
    form_class = BoatForm
    success_url = '/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()

        initial['BoatName'] = get_object_or_404(Boat, pk=self.kwargs['pk']).BoatName
        initial['PyNumber'] = get_object_or_404(Boat, pk=self.kwargs['pk']).PyNumber

        return initial
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


class BoatNewFormView(UpdateView):
    template_name = 'boat/boat_form.html'
    form_class = BoatForm
    success_url = '/'
    model = Boat
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class BoatDeleteView(DeleteView):
    # specify the model you want to use
    template_name = 'boat/boat_confirm_delete.html'
    model = Boat
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"

# Racer registration classes
class RacerListView(ListView):
    model = Racer
    template_name="racer/racer_list.html"

class RacerEditFormView(UpdateView):
    template_name = 'racer/racer_form.html'
    form_class = RacerForm
    success_url = '/'
    model = Racer

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()

        initial['HelmName'] = get_object_or_404(Racer, pk=self.kwargs['pk']).HelmName
        initial['CrewName'] = get_object_or_404(Racer, pk=self.kwargs['pk']).CrewName
        initial['SailNumber'] = get_object_or_404(Racer, pk=self.kwargs['pk']).SailNumber
        initial['Boat'] = get_object_or_404(Racer, pk=self.kwargs['pk']).Boat

        return initial
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


class RacerNewFormView(FormView):
    template_name = 'racer/racer_form.html'
    form_class = RacerForm
    success_url = '/'
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class RacerDeleteView(DeleteView):
    # specify the model you want to use
    template_name = 'racer/racer_confirm_delete.html'
    model = Racer
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"

class ResultsHomeView(TemplateView):
    template_name = 'results/resultsIndex.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['races'] = Race.objects.all()
        return context

class RaceResultsView(TemplateView):
    template_name = 'results/results.html'
    def get_context_data(self, pk):
        context = super().get_context_data()

        raceEvents = RaceEvent.objects.filter((Q(Status=0)|Q(Status=1)), Race_id=pk)

        mostLaps = raceEvents.order_by('-LapsComplete')[0].LapsComplete
        raceStartTime = Race.objects.get(pk=pk).StartTime

        raceEventsReturn = []

        for raceEvent in raceEvents:
            elapsedTime = (raceEvent.FinishTime - timezone.make_aware(datetime.datetime.combine(raceEvent.FinishTime.date(), raceStartTime))).seconds
            correctedTime = (elapsedTime * mostLaps * 1000)/(raceEvent.Racer.Boat.PyNumber * raceEvent.LapsComplete)
            raceEventsReturn.append({'raceEvent': raceEvent, 'elapsedTime':elapsedTime, 'correctedTime':correctedTime})
        
        context['pk'] = pk
        context['raceEvents'] = sorted(raceEventsReturn, key=lambda k: k['correctedTime'])
        return context


# Management views

class OodHomeView(TemplateView):
    template_name = 'manage/OodHomePage.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['races'] = Race.objects.all()
        context['racers'] = Racer.objects.all()

        return context

class RunRaceView(TemplateView):
    template_name = 'manage/run.html'
    def get_context_data(self, pk):
        context = super().get_context_data()
        context['racePK'] = pk

        return context

## Race views

class RaceEditFormView(UpdateView):
    template_name = 'race/race_form.html'
    form_class = RaceForm
    model = Race
    success_url = '/manage/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()

        initial['RaceNumber'] = get_object_or_404(Race, pk=self.kwargs['pk']).RaceNumber
        initial['StartTime'] = get_object_or_404(Race, pk=self.kwargs['pk']).StartTime
        initial['RaceLength'] = get_object_or_404(Race, pk=self.kwargs['pk']).RaceLength
        initial['RaceType'] = get_object_or_404(Race, pk=self.kwargs['pk']).RaceType

        return initial
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save()        
        return super().form_valid(form)


class RaceNewFormView(FormView):
    template_name = 'race/race_form.html'
    form_class = RaceForm
    success_url = '/manage/'
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class RaceDeleteView(DeleteView):
    # specify the model you want to use
    template_name = 'race/race_confirm_delete.html'
    model = Race
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = '/manage/'

## Race results AJAX calls
@method_decorator(csrf_exempt, name='dispatch')
class AjaxAddLap(View):
    def post(self, request):
        raceEvent = RaceEvent.objects.get(pk=request.POST['raceEventID'])
        raceEvent.LapsComplete = raceEvent.LapsComplete + int(request.POST['change'])
        raceEvent.save()
        return HttpResponse('Done')

@method_decorator(csrf_exempt, name='dispatch')
class AjaxChangeStatus(View):
    def post(self, request):
        raceEvent = RaceEvent.objects.get(pk=request.POST['raceEventID'])
        if request._post['status'] == '0':
            raceEvent.FinishTime = datetime.datetime.now(tz=timezone.utc)
        else:
            raceEvent.FinishTime = None

        if request._post['status']:
            raceEvent.Status = request._post['status']
        else:
            raceEvent.Status = None

        raceEvent.save()
        return HttpResponse('Done')
        
@method_decorator(csrf_exempt, name='dispatch')
class AjaxGetResults(View):
    def get(self, request, pk):
        racers = RaceEventSerializer(RaceEvent.objects.filter((Q(Status=0)|Q(Status=None)), Race__pk=pk), many=True)
        return JsonResponse(racers.data, safe=False)
