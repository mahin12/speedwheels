from django.contrib import admin, messages
from django.core.mail import send_mail

from trydjango.settings import EMAIL_HOST_USER
from .models import *


class ReportAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if obj.status == "REJECTED" or obj.status == "ACCEPTED":
                messages.success(request, "Status was sent to the user")
                subject = 'Car repair request status'
                message = 'Hope you are enjoying your Quarantine time. #KitaJagaKita. Here is your car repair request status. You request was {}'.format(
                    obj.status)
                recipient = str(obj.user.email)
                send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        super(ReportAdmin, self).save_model(request, obj, form, change)


admin.site.register(Reservation)
admin.site.register(Report, ReportAdmin)
