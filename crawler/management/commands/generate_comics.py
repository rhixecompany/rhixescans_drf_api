import json
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        def save_comic():
            base = settings.BASE_DIR
            comics_file = str(base / "comics.json")
            with open(comics_file) as f:
                comics_data = json.load(f)
                for c in comics_data:
                    description = c["description"]
                    updated_at = c["updated_at"]
                    pprint(
                        {
                            # "comic": c,
                            "description": description,
                            "updated_at": updated_at,
                        }
                    )

            return

        save_comic()
