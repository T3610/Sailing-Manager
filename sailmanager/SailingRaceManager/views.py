from django.views.generic import ListView, TemplateView, FormView, View, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from SailingRaceManager.models import Boat, Race, Racer, RaceEvent, OfficialEvent
from SailingRaceManager.forms import BoatForm, RacerForm, RaceForm, OfficialForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, request
from .serializers import RaceEventSerializer
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime, csv, uuid
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexPage(TemplateView):
    template_name = 'index.html'


# Boat management classes
class BoatListView(LoginRequiredMixin,ListView):
    model = Boat
    template_name="boat/boat_list.html"

class BoatEditFormView(LoginRequiredMixin,UpdateView):
    template_name = 'boat/boat_form.html'
    model = Boat
    form_class = BoatForm
    success_url = '/boats'

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


class BoatNewFormView(LoginRequiredMixin,CreateView):
    template_name = 'boat/boat_form.html'
    form_class = BoatForm
    success_url = '/boats'
    model = Boat
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class BoatDeleteView(LoginRequiredMixin,DeleteView):
    # specify the model you want to use
    template_name = 'boat/boat_confirm_delete.html'
    model = Boat
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/boats"

# Start timing classes

class StartingOrderView(TemplateView):
    template_name="startTimings/timings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['races'] = Race.objects.filter(Date__gte=datetime.date.today(), Date__lt=datetime.date.today() + relativedelta(weeks=1))
        if 'race' in self.request.GET:
            race = Race.objects.get(pk=self.request.GET['race'])
            raceEvents = RaceEvent.objects.filter(Race=race)
            enteredBoats = raceEvents.values_list('Racer__Boat__PyNumber','Racer__Boat__BoatName').distinct()
            enteredBoatsOrdered = sorted(enteredBoats, key=lambda x: x[0], reverse=True)
            slowestBoatPy = enteredBoatsOrdered[0][0]

            slowestBoatCorrectTime = race.RaceLength*1000/slowestBoatPy

            boats = []
            for boat in enteredBoatsOrdered:
                boats.append({
                    'boatName': boat[1],
                    'boatPY': boat[0],
                    'startTime': round(race.RaceLength - slowestBoatCorrectTime*boat[0]/1000),
                })
            context['boats'] = boats
            context['thisRace'] = race

        return context

# Racer registration classes
class RacerListView(TemplateView):
    template_name="racer/racer_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        signUpUUID = self.request.session.get('signUpUUID')
        if signUpUUID:
            context['signUpUUID'] = signUpUUID

        context['races'] = Race.objects.all()
        if 'race' in self.request.GET:
            context['thisRace'] = Race.objects.get(pk=self.request.GET['race'])
            context['raceEvents'] = RaceEvent.objects.filter(Race=context['thisRace'])

        return context

class RacerEditFormView(UpdateView):
    template_name = 'racer/racer_form.html'
    form_class = RacerForm
    success_url = '/racers'
    model = Racer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['races'] = Race.objects.all()
        racer = get_object_or_404(Racer, pk=self.kwargs['pk'])

        context['racesEntered'] = list(RaceEvent.objects.filter(Racer=racer).values_list('Race_id',flat=True))
        return context

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
        racesEntered = self.request.POST.getlist("racesEntered[]")
        allRacesID = list(Race.objects.all().values_list('id',flat=True))

        racesNotEntered = []
        for raceID in allRacesID:
            if str(raceID) not in racesEntered:
                racesNotEntered.append(raceID)

        for race in racesEntered:
            newRaceEvent, created = RaceEvent.objects.get_or_create(Racer=self.object, Race_id=race)
            if created:
                newRaceEvent.save()
        for race in racesNotEntered:
            try:
                RaceEvent.objects.filter(Racer=self.object, Race_id=race).delete()
            except:
                pass

        return super().form_valid(form)


class RacerNewFormView(FormView):
    template_name = 'racer/racer_form.html'
    form_class = RacerForm
    success_url = '/racers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        dateInAWeek = today + relativedelta(weeks=1)
        context['races'] = Race.objects.filter(Date__gte=today, Date__lt=dateInAWeek) # Show dates from today to a weeks time
        return context

    
    def form_valid(self, form):
        if len(self.request.POST.getlist("racesEntered[]")) < 1:
            return super().form_invalid(form)

        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        if 'signUpUUID' not in self.request.session:
            self.object.SignedUpBy = uuid.uuid4().hex
            self.object.save()
            self.request.session['signUpUUID'] = self.object.SignedUpBy
        else:
            self.object.SignedUpBy = self.request.session['signUpUUID']
            self.object.save()

        racesEntered = self.request.POST.getlist("racesEntered[]")
        for race in racesEntered:
            newRaceEvent, created = RaceEvent.objects.get_or_create(Racer=self.object, Race_id=race)

        return super().form_valid(form)


class OfficialNewFormView(FormView):
    #View for race officials
    template_name = 'official/official_form.html'
    form_class = OfficialForm
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['races'] = Race.objects.all()
        return context
        
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        racesEntered = self.request.POST.getlist("racesEntered[]")
        for race in racesEntered:
            newRaceEvent, created = OfficialEvent.objects.get_or_create(Official=self.object, Race_id=race)


        return super().form_valid(form)

class RacerDeleteView(DeleteView):
    # specify the model you want to use
    template_name = 'racer/racer_confirm_delete.html'
    model = Racer
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/manage"

class ResultsHomeView(TemplateView):
    template_name = 'results/resultsIndex.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['races'] = Race.objects.all()
        return context

def getResults(racepk):
    race = Race.objects.get(pk=racepk)

    context = {}
    context['pk'] = racepk
    context['race'] = race
    context['retirements'] = RaceEvent.objects.filter(Status=1, Race_id=racepk)

    if race.RaceType == 0: # Handicap
        raceEvents = RaceEvent.objects.filter(Status=0, Race_id=racepk)

        if len(raceEvents) > 0:
            mostLaps = raceEvents.order_by('-LapsComplete')[0].LapsComplete
            raceStartTime = race.StartTime

            raceEventsReturn = []

            for raceEvent in raceEvents:
                elapsedTime = (raceEvent.FinishTime - raceStartTime).seconds
                correctedTime = (elapsedTime * mostLaps * 1000)/(raceEvent.Racer.Boat.PyNumber * raceEvent.LapsComplete)
                raceEventsReturn.append({'raceEvent': raceEvent, 'elapsedTime':elapsedTime, 'correctedTime':correctedTime, 'lapsComplete':raceEvent.LapsComplete})
            

            context['raceEvents'] = sorted(raceEventsReturn, key=lambda k: k['correctedTime'])

    elif race.RaceType == 1: # Pursuit
        raceEvents = RaceEvent.objects.filter(Status=0, Race_id=racepk)

        raceEvents = raceEvents.order_by('-LapsComplete', 'FinishTime')

        raceEventsReturn=[]

        for raceEvent in raceEvents:
            raceEventsReturn.append({'raceEvent': raceEvent})

        context['raceEvents'] = raceEventsReturn    

    context['raceOfficials'] = OfficialEvent.objects.filter(Race=race)

    return context

class RaceResultsView(TemplateView):
    template_name = 'results/results.html'
    def get_context_data(self, pk):
        context = super().get_context_data()
        context = {**context, **getResults(pk)}

        return context

class RaceResultsDetailedView(View):
    def get(self, request, pk):
        race = Race.objects.get(pk=pk)
        raceEvents = getResults(pk)['raceEvents']
        results = []
        position = 1
        for raceEvent in raceEvents:
            event = {}
            helmName = raceEvent['raceEvent'].Racer.HelmName
            crewName = raceEvent['raceEvent'].Racer.CrewName
            sailNumber = raceEvent['raceEvent'].Racer.SailNumber
            boatClass = raceEvent['raceEvent'].Racer.Boat.BoatName

            event = {'Position':position, 'Helm Name': helmName, 'Crew Name':crewName, 'Sail Number':sailNumber, 'Class':boatClass}

            if race.RaceType == 0:
                lapsComplete = raceEvent['lapsComplete']
                elapsedTime = raceEvent['elapsedTime']
                correctedTime = raceEvent['correctedTime']

                event = {**event, 'Laps Complete': lapsComplete, 'Elapsed Time (seconds)':elapsedTime, 'Corrected Time (seconds)':correctedTime}

            results.append(event)
            position = position + 1 

        
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Race-results-%s.csv"'%race.RaceNumber},
        )
        writer = csv.DictWriter(response, fieldnames=list(results[0].keys()))
        writer.writeheader()
        for data in results:
            writer.writerow(data)

        return response


# Management views

class OodHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'manage/OodHomePage.html'
    def get_context_data(self):
        context = super().get_context_data()
        if 'previous' in self.request.GET:
            if self.request.GET['previous'] == 'true':
                context['races'] = Race.objects.all()
                context['newValueForPreviousParam'] = "false"
                context['timespanBtn'] = "only upcoming"
            else:
                today = datetime.datetime.today()
                context['races'] = Race.objects.filter(Date__gte=today)
                context['newValueForPreviousParam'] = "true"
                context['timespanBtn'] = "all"
        else:
            today = datetime.datetime.today()
            context['races'] = Race.objects.filter(Date__gte=today)
            context['newValueForPreviousParam'] = "true"
            context['timespanBtn'] = "all"
    
        context['racesForEntries'] = Race.objects.all()
        if 'racesForEntries' in self.request.GET:
            context['thisRace'] = Race.objects.get(pk=self.request.GET['racesForEntries'])
            context['raceEvents'] = RaceEvent.objects.filter(Race=context['thisRace'])

        return context



class RunRaceView(LoginRequiredMixin, TemplateView):
    template_name='manage/runRace.html'

    def get_context_data(self, pk):
        context = super().get_context_data()
        context['race'] = Race.objects.get(pk=pk)

        return context

## Race views

class RaceEditFormView(LoginRequiredMixin, UpdateView):
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


class RaceNewFormView(LoginRequiredMixin, FormView):
    template_name = 'race/race_form.html'
    form_class = RaceForm
    success_url = '/manage/'
    
    def form_valid(self, form):
        self.object = form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class RaceDeleteView(LoginRequiredMixin, DeleteView):
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
class AjaxSetRaceStart(View):
    def post(self, request, pk):
        race = Race.objects.get(pk=pk)
        if 'clear' in request.POST:
            race.StartTime = None
        else:
            race.StartTime = timezone.now()+datetime.timedelta(seconds=int(request.POST['timedelta']))
            race.save()
            return HttpResponse(race.StartTime.strftime('%H:%M'))
        race.save()
        return HttpResponse('Done')
        
@method_decorator(csrf_exempt, name='dispatch')
class AjaxGetResults(View):
    def get(self, request, pk):
        racers = RaceEventSerializer(RaceEvent.objects.filter((Q(Status=0)|Q(Status=None)), Race__pk=pk).order_by('-Status','Racer__Boat__PyNumber'), many=True)
        return JsonResponse(racers.data, safe=False)

class UploadBoatList(TemplateView):
    template_name='boat/boat_uploadCSV.html'

    def post(self, request):
        print('POST')
        if 'csvFile' in request.FILES:
            if request._post['actionSelect'] == 'DELETE':
                Boat.objects.all().delete()
            paramFile = request.FILES['csvFile'].read().decode("utf-8-sig")	
            lines = paramFile.split("\n") 
            for line in lines[1:]:      
                line = line.replace('\r', '')     			
                fields = line.split(",")
                newBoat = Boat(BoatName=fields[0].upper(),PyNumber=fields[1])
                newBoat.save()
        return redirect('/boats')