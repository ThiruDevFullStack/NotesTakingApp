from django.db import models

# Create your models here.
class NotesTaking(models.Model):
    heading=models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    modified_date = models.DateTimeField()


    def __str__(self):
        return self.heading

