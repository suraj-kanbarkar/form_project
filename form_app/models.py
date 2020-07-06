from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserFormDetails(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    upload_pdf = models.FileField(blank=True, null=True, upload_to='pdf_files/')
    date_of_birth = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s" % (self.user, self.email, self.first_name, self.last_name, self.image,
                                               self.upload_pdf, self.date_of_birth, self.submission_date, self.notes)

