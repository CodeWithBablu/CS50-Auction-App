from django.contrib import admin
from .models import Listing,WatchList,User,Comment,Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Bid)