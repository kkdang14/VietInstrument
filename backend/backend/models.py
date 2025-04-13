from django.db import models

class Vqa_predictions(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.image.name