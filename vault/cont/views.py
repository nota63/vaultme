import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import Cont
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

# Create your views here.

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, f'Contact {contact.name} saved successfully')
            return redirect('add_contact')
    else:
        form = ContactForm
    return render(request, 'cont/add_contacts.html', {'form': form})


@login_required
def view_contacts(request):
    search_query = request.GET.get('search', '')
    filter_option = request.GET.get('filter', '')

    contacts = Cont.objects.filter(user=request.user)

    if search_query:
        contacts = contacts.filter(name__icontains=search_query)

    if filter_option:
        if filter_option == 'active':
            contacts = contacts.filter(active=True)
        elif filter_option == 'inactive':
            contacts = contacts.filter(active=False)

    return render(request, 'cont/view_contacts.html', {'data': contacts})

@login_required
def delete_contact(request, cont_id):
    contact = get_object_or_404(Cont, id=cont_id)
    contact.delete()
    messages.success(request, 'contact deleted successfully')
    return redirect('view_contacts')

@login_required
def download_contacts(request):
    # Create the response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Name', 'Relation', 'Contact', 'Type', 'Active'])

    # Fetch contacts data
    contacts = Cont.objects.filter(user=request.user)
    for contact in contacts:
        writer.writerow([contact.name, contact.relation, contact.contact, contact.type, contact.active])

    return response


@login_required
def analytics_view(request):
    user=request.user
    contacts=Cont.objects.filter(user=user)
    total_contacts = contacts.count()
    active_contacts = Cont.objects.filter(user=request.user,active=True).count()
    inactive_contacts = Cont.objects.filter(user=request.user,active=False).count()

    # Recent contacts calculation removed due to absence of `created_at` field
    recent_contacts = 0  # Set to 0 or remove if not applicable

    contacts_by_type = Cont.objects.values('type').annotate(count=Count('type')).order_by('type')

    context = {
        'total_contacts': total_contacts,
        'active_contacts': active_contacts,
        'inactive_contacts': inactive_contacts,
        'recent_contacts': recent_contacts,
        'contacts_by_type': contacts_by_type,
    }
    return render(request, 'cont/analytics.html', context)