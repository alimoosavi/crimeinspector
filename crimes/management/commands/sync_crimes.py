from django.core.management.base import BaseCommand
from crimes.services import CrimesFetcherJob


class Command(BaseCommand):
    """
        This class is a django management command and its main goal is to create
        a cli interface to run crime synchronizer job
    """
    help = 'Sync crimes with google'

    def handle(self, *args, **options):
        CrimesFetcherJob().run()
