from django.contrib import admin
from room.models import Room, Reservation, Image


class ImageTabularAdmin(admin.TabularInline):
    model = Image
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [ImageTabularAdmin,]


admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Image)
