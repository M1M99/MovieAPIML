import pandas as pd
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Load movies from XLSX"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("real_movies_sample1.xlsx")

        for _, row in df.iterrows():
            Movie.objects.get_or_create(
                title=row["Title"],
                description=row["Description"],
                image_url=row["ImageUrl"]
            )

        self.stdout.write(self.style.SUCCESS("Movies loaded successfully!"))
