from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.templatetags.static import static
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
import openpyxl
from openpyxl import Workbook
from django.urls import reverse
from .models import GuestList, Guest
from django.conf import settings
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.core.cache import cache
import tempfile
import os
from django.core.management import call_command
import logging
from openpyxl.utils.exceptions import InvalidFileException
import datetime
# Create your views here.

logger = logging.getLogger(__name__)

def home(request):
    guests = Guest.objects.all()

    if request.method == 'POST':
        if 'send_invitations' in request.POST:
            for guest in guests:
                if not guest.email_sent:
                    if '@' not in guest.email:
                        # Skip sending email if the email does not contain '@'
                        continue
                    
                    try:
                        static_image_url = "https://dl.dropboxusercontent.com/scl/fi/ruo4jlhoj3ajjobe7yfe4/email_envalope.png?rlkey=imzfzzp9dghevrqneuxcc1s0k&st=ssjaknly"
                        
                        context = {
                            'guest_name': guest.name,
                            'invitation_url': f"https://wedding-sjyr.onrender.com/invitation/{guest.name}/{guest.identification}",
                            'static_image_url': static_image_url
                        }
                        
                        if guest.country.lower() == 'israel':
                            subject = 'הזמנה לחתונה גיא ואליה'
                            message = render_to_string('main/email_body_he.html', context)
                        else:
                            subject = 'The Wedding of Aaliyah and Guy'
                            message = render_to_string('main/email_body_en.html', context)

                        send_mail(
                            subject,
                            '',  # Empty plain text message
                            'guyandaaliyahwedding@gmail.com',
                            [guest.email],
                            fail_silently=False,
                            html_message=message,
                        )
                        guest.email_sent = True
                        guest.save()
                    except AttributeError:
                        message = f'Hi {guest.name}, here is your invitation.'

            messages.success(request, "Invitations sent successfully!")
            return redirect('home')
        elif 'import_guests' in request.POST:
            if 'guest_file' in request.FILES:
                guest_file = request.FILES['guest_file']
                file_extension = os.path.splitext(guest_file.name)[1]
                if file_extension not in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
                    messages.error(request, "Invalid file format. Please upload an Excel file.")
                    return redirect('home')

                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                        for chunk in guest_file.chunks():
                            temp_file.write(chunk)
                    temp_file_path = temp_file.name
                    logger.info(f"Temporary file created at: {temp_file_path}")

                    call_command('import_guests', temp_file_path)
                    messages.success(request, "Guests imported successfully!")
                except InvalidFileException:
                    messages.error(request, "Failed to load or process the workbook: Invalid file format.")
                except Exception as e:
                    messages.error(request, f"Failed to import guests: {str(e)}")
                    logger.error(f"Failed to import guests: {e}")
                finally:
                    os.remove(temp_file_path)
                    logger.info(f"Temporary file {temp_file_path} removed.")
            else:
                messages.error(request, "No file uploaded.")
            return redirect('home')

    # Ensure fetching the latest data
    guests = Guest.objects.all()
    return render(request, 'main/home.html', {'show_navbar': True, 'guests': guests})


def export_guests(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Guests"

    headers = [
        'name', 'email', 'phone', 'country', 'attending',
        'number_of_guests_invited', 'number_of_guests_attending', 'message', 'email_sent', 'id'
    ]
    ws.append(headers)

    for guest in Guest.objects.all():
        row = [
            guest.name,
            guest.email,
            guest.phone,
            guest.country,
            guest.attending,
            guest.number_of_guests_invited,
            guest.number_of_guests_attending,
            guest.message,
            guest.email_sent,
            guest.identification
        ]
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=guest_list.xlsx'
    wb.save(response)
    return response


def serve_apng(request):
    return redirect('https://d16bqg9cd7djd.cloudfront.net/en_animation.webp')
    

def invitation(request, name, identification):
    # Determine if the navbar should be shown based on 'admin' access
    show_navbar = (name.lower() == 'admin')

    # Admin special case
    if show_navbar:
        admin_guest = Guest(name='Admin', id=0, country='N/A')  # Admin dummy guest with a dummy country
        return render(request, 'main/invitation.html', {
            'guest': admin_guest,
            'show_navbar': show_navbar,
            'country': admin_guest.country  # Include country in context
        })

    # Attempt to fetch the guest list by name
    guest_list_name = 'Main Guest List'
    try:
        guest_list = GuestList.objects.get(name=guest_list_name)
    except GuestList.DoesNotExist:
        return HttpResponse("Guest List not found.")

    # Fetch the guest by identification
    guest = guest_list.guests.filter(identification=identification).first()
    if not guest or guest.name.lower() != name.lower():
        # Guest not found or name does not match, do not show navbar
        return render(request, 'main/invitation.html', {
            'error': 'Guest not found.',
            'show_navbar': False
        })

    # Render for regular guest, include country in context
    return render(request, 'main/invitation.html', {
        'guest': guest,
        'show_navbar': False,
    })




def guest_response(request, guest_id):
    guest = get_object_or_404(Guest, pk=guest_id)
    if request.method == 'POST':
        response = request.POST.get('response')
        if response == 'not_attending':
            guest.attending = False
            guest.number_of_guests_attending = 0
        elif response == 'attending':
            guest.attending = True
            guest.number_of_guests_attending = request.POST.get('num_guests', 0)
        guest.save()
        return redirect(reverse('invitation', args=[guest.name, guest.identification]))  # Redirect to the invitation page or a confirmation page
    return render(request, 'main/invitation.html', {'guest': guest})



@never_cache
def guest_list(request):
    guests = Guest.objects.all()
    logger.info(f"Fetched {len(guests)} guests")
    for guest in guests:
        logger.info(f"Guest: {guest.name}, Attending: {guest.attending}, Guests Attending: {guest.number_of_guests_attending}")
    return render(request, 'main/guest_list.html', {'guests': guests, 'show_navbar': True})


@never_cache
def statistics(request):
    total_parties = Guest.objects.count()
    attending_parties = Guest.objects.filter(attending=True).count()
    not_attending_parties = Guest.objects.filter(attending=False).count()
    not_confirmed_parties = Guest.objects.filter(attending=None).count()
    
    total_guests_invited = Guest.objects.aggregate(Sum('number_of_guests_invited'))['number_of_guests_invited__sum'] or 0
    total_guests_attending = Guest.objects.aggregate(Sum('number_of_guests_attending'))['number_of_guests_attending__sum'] or 0
    
    return render(request, 'main/statistics.html', {
        'total_parties': total_parties,
        'attending_parties': attending_parties,
        'not_attending_parties': not_attending_parties,
        'not_confirmed_parties': not_confirmed_parties,
        'total_guests_invited': total_guests_invited,
        'total_guests_attending': total_guests_attending,
        'show_navbar': True
    })
