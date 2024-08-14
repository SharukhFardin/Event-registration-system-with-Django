from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "location", "available_slots")
    search_fields = ("title", "description", "location")
    list_filter = ("date", "location")
    ordering = ("-date",)
    inlines = [EventRegistrationInline]


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "timestamp")
    search_fields = ("user__username", "event__title")
    list_filter = ("event", "user")
    ordering = ("-timestamp",)


# Register the models with the admin site
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
