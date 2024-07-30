from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Passwords
from .forms import PasswordForm
from django.contrib import messages
from django.db.models import Count
from django.db.models import Count, Q
# START YOUR VIEWS HERE
@login_required
def store_passwords(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.user = request.user
            password.save()
            messages.success(request, f'{password.type} at {password.type} saved to SQlite3')
            return redirect('store_passwords')
    else:
        form = PasswordForm()
    return render(request, 'hash/store_passwords.html', {'form': form})

@login_required
def view_passwords(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', '')

    passwords = Passwords.objects.filter(user=request.user)

    if query:
        passwords = passwords.filter(id_name__icontains=query)

    if filter_type:
        passwords = passwords.filter(type=filter_type)

    return render(request, 'hash/view_passwords.html', {'data': passwords, 'query': query, 'filter_type': filter_type})

@login_required
def delete_passwords(request, passwords_id):
    password=get_object_or_404(Passwords,id=passwords_id)
    password.delete()
    messages.success(request,f'{password.type} of {password.username} removed from SQLite3')
    return redirect('view_passwords')


@login_required
def analytics_view_passwords(request):
    passwords = Passwords.objects.filter(user=request.user)

    # Total count
    total_passwords = passwords.count()

    # Count by type
    types_count = passwords.values('type').annotate(count=Count('type'))

    # Active vs Inactive passwords
    active_passwords = passwords.filter(is_active=True).count()
    inactive_passwords = passwords.filter(is_active=False).count()

    # Count by date created (last 6 months)
    date_counts = passwords.extra({'created_date': "date(created_date)"}).values('created_date').annotate(count=Count('id')).order_by('created_date')

    context = {
        'total_passwords': total_passwords,
        'types_count': types_count,
        'active_passwords': active_passwords,
        'inactive_passwords': inactive_passwords,
        'date_counts': date_counts,
    }
    return render(request, 'hash/analytics_view_passwords.html', context)