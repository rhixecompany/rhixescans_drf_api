from django.db import models


class NewManager(models.QuerySet):
    def get_ongoing(self):
        return self.filter(status="Ongoing")

    def get_completed(self):
        return self.filter(status="Completed")
