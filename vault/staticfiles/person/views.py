import zipstream
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from . import models
from .forms import PersonForm
from .models import Person
from django.contrib import messages
import csv
import os
import zipfile
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.conf import settings
import zipstream
from django.http import HttpResponse
from .models import Person
from django.core.files.storage import default_storage
from django.db.models import Count
from datetime import datetime


# Create your views here.
@login_required
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            messages.success(request, 'Person details saved successfully')
            return redirect('add_person')
    else:
        form = PersonForm()
    return render(request, 'person/add_person.html', {'form': form})


@login_required
def view_persons(request):
    query = request.GET.get('q')
    connection_filter = request.GET.get('connection')
    type_filter = request.GET.get('type')

    persons = Person.objects.filter(user=request.user)

    if query:
        persons = persons.filter(name__icontains=query)

    if connection_filter and connection_filter != 'all':
        persons = persons.filter(connection=connection_filter)

    if type_filter and type_filter != 'all':
        persons = persons.filter(type=type_filter)

    return render(request, 'person/view_persons.html', {
        'data': persons,
        'query': query,
        'connection_filter': connection_filter,
        'type_filter': type_filter,
    })


@login_required
def delete_persons(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    messages.success(request, f'details of {person.name} deleted success')
    return redirect('view_persons')


@login_required
def download_persons(request):
    # Create a BytesIO object to hold the zip data
    zip_buffer = BytesIO()

    # Create a zip file
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Get all persons with images
        persons = Person.objects.filter(user=request.user)
        for person in persons:
            if person.profile_pic:
                # Get the image path
                image_path = default_storage.path(person.profile_pic.name)
                # Add the image file to the zip
                with open(image_path, 'rb') as image_file:
                    zip_file.writestr(os.path.basename(image_path), image_file.read())

    # Ensure the zip buffer is positioned at the beginning before reading
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="person_images.zip"'
    return response

@login_required
def analytics(request):
    # Existing data processing
    total_persons = Person.objects.filter(user=request.user).count()

    # Correct use of Count for aggregations
    connection_distribution = Person.objects.filter(user=request.user).values('connection').annotate(count=Count('id'))
    social_distribution = Person.objects.filter(user=request.user).values('type').annotate(count=Count('id'))
    top_connections = Person.objects.filter(user=request.user).values('name').annotate(count=Count('id')).order_by(
        '-count')[:5]
    recent_activities = Person.objects.filter(user=request.user).values('name').annotate(count=Count('id')).order_by(
        '-count')[:5]
    average_connection = Person.objects.filter(user=request.user).values('connection').annotate(count=Count('id'))

    # New data for the additional chart
    social_media_usage = Person.objects.filter(user=request.user).values('type').annotate(count=Count('id'))

    context = {
        'total_persons': total_persons,
        'connection_distribution': connection_distribution,
        'social_distribution': social_distribution,
        'top_connections': top_connections,
        'recent_activities': recent_activities,
        'average_connection': average_connection,
        'social_media_usage': social_media_usage,  # Pass new data
    }
    return render(request, 'person/analytics.html', context)