from django.db import models

class data(models.Model):
    time=models.TimeField(primary_key=True)
    data_records=models.JSONField()
    data_filtered=models.JSONField()

