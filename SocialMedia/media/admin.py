from django.contrib import admin
from media.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Likes)
admin.site.register(Comment)
