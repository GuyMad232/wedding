# from django.core.management.base import BaseCommand
# from openpyxl import Workbook
# from main.models import Guest, GuestList
# import os
# from django.conf import settings

# class Command(BaseCommand):
#     help = 'Exports guests to an Excel file.'

#     def handle(self, *args, **options):
#         # Create a workbook and select the active worksheet
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Guests"

#         # Add the headers
#         headers = [
#             'name', 'email', 'phone', 'country', 'attending',
#             'number_of_guests_invited', 'number_of_guests_attending', 'message', 'email_sent','id'
#         ]
#         ws.append(headers)

#         # Add the data rows
#         for guest in Guest.objects.all():
#             row = [
#                 guest.name,
#                 guest.email,
#                 guest.phone,
#                 guest.country,
#                 guest.attending,
#                 guest.number_of_guests_invited,
#                 guest.number_of_guests_attending,
#                 guest.message,
#                 guest.email_sent,
#                 guest.identification
#             ]
#             ws.append(row)

#         # Save the workbook to the file
#         filename = os.path.join(settings.BASE_DIR, 'resources/guest_list.xlsx')
#         wb.save(filename)
#         self.stdout.write(self.style.SUCCESS('Guests exported successfully.'))
