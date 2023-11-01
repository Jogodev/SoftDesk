from django.contrib import admin

from .models import Comments, Contributors, Issues, Projects


admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)
admin.site.register(Contributors)
