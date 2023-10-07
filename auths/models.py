from django.db import models
# import datetime
# import os

# def filepath(request, filename):
#     old_filename = filename
#     timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
#     filename = "%s%s" % (timeNow, old_filename)
#     return os.path.join('profile/', filename)     


# Create your models here.
class userinfo(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.BinaryField()

    def __str__(self):
        return self.email