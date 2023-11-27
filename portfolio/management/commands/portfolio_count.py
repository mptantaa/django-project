from django.core.management.base import BaseCommand
from portfolio.models import Portlofios

class Command(BaseCommand):
    help = 'Get count portfolio elements'

    def handle(self, *args, **options):
        portfolios = Portlofios.objects.all()
        total_portfolios = portfolios.count()
        self.stdout.write(self.style.SUCCESS(f'Total portfolio elements: {total_portfolios}'))
