from django.contrib import admin

# Register your models here.
from Mryang_App import models

admin.site.register([models.User, models.UserAlbum])
