from django.core.management.base import BaseCommand
from crimes.services import CrimesFetcherJob


class Command(BaseCommand):
    help = 'Sync crimes with google'

    def handle(self, *args, **options):
        CrimesFetcherJob().run()
