import re
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from symptoms.models import Symptom
from symptoms.correlation import DATASET_PATH

class Command(BaseCommand):
    help = "Load symptom names from a disease-symptom CSV file."

    def add_arguments(self, parser):
        parser.add_argument("--file", default=str(DATASET_PATH))

    def handle(self, *args, **options):
        path = options["file"]
        try:
            frame = pd.read_csv(path)
        except Exception as exc:
            raise CommandError(f"Could not read CSV: {exc}")
        if "disease" not in frame.columns:
            raise CommandError("CSV must contain a 'disease' column.")
        columns = [c for c in frame.columns if c.lower() != "disease"]
        created = 0
        for column in columns:
            name = re.sub(r"_+", " ", column.replace("-", " ")).strip().title()
            _, was_created = Symptom.objects.get_or_create(name=name)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(columns)} symptom names; created {created} new records."
        ))
