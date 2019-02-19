from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	name = models.CharField(max_length = 100, null = True)
	surname = models.CharField(max_length = 100, null = True)
	date_of_birth = models.DateTimeField(max_length = 100, null = True)
	phone = models.CharField(max_length = 100, null = True)
	email = models.CharField(max_length = 100, null = True)


