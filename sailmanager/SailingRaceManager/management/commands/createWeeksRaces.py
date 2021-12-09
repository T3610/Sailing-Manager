from django.core.management.base import BaseCommand, CommandError
from SailingRaceManager.models import Race
import datetime

class Command(BaseCommand):
    help = 'Creates 2 races on the next Sunday - run on a wednesday'

    def handle(self, *args, **options):
        today = datetime.date.today()

        timedelta = datetime.timedelta(days=6-today.weekday())

        sunday = today+timedelta

        if sunday.day < 8:
            raceType = 1    # Pursuit race on the first sunday of the month
        else:
            raceType = 2    # Handicap race every other weekend

        for i in range(1,3):
            race = Race(RaceNumber=i, Date=sunday, RaceType=raceType)
            race.save()

        print("Races created")