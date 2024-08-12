from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.db.models.functions import ExtractMonth
from .forms import PrivateForm
from .models import Private
from django.contrib import messages
import zipfile
import io
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Count, Avg
from django.db.models import Count, Avg
# Create your views here.
@login_required
def store_pics(request):
    if request.method == 'POST':
        form = PrivateForm(request.POST, request.FILES)
        if form.is_valid():
            private = form.save(commit=False)
            private.user = request.user
            private.save()
            messages.success(request, f'Image {private.name} of {private.size} saved to database')
            return redirect('store_pics')
    else:
        form = PrivateForm()
    return render(request, 'private/store_pics.html', {'form': form})


def view_pis(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    # Filter data based on search query and category
    if search_query:
        data = Private.objects.filter(user=request.user, name__icontains=search_query) | Private.objects.filter(
            user=request.user, description__icontains=search_query)
    else:
        data = Private.objects.filter(user=request.user)

    if category_filter:
        data = data.filter(category=category_filter)

    # Get distinct categories for filter dropdown
    categories = Private.objects.values_list('category', flat=True).distinct()

    return render(request, 'private/view_pics.html', {'data': data, 'categories': categories})


def download_images(request):
    # Get all images for the logged-in user
    images = Private.objects.filter(user=request.user)

    # Create an in-memory ZIP file
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for image in images:
            image_file = image.image
            image_name = f"{image.name}.jpg"  # Modify if needed
            zip_file.writestr(image_name, image_file.read())

    # Prepare the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    return response

def delete_pics(request, pic_id):
    pic=get_object_or_404(Private, id=pic_id)
    pic.delete()
    messages.success(request,f'{pic.name} has been deleted')
    return redirect('view_pis')


@login_required
def analytics_view_private(request):
    # Fetch data for the logged-in user
    private_pics = Private.objects.filter(user=request.user)

    # Aggregate data for charts
    category_counts = private_pics.values('category').annotate(count=Count('category')).values('category', 'count')
    size_distribution = private_pics.values('size').annotate(count=Count('size')).values('size', 'count')
    tag_counts = private_pics.values('tags').annotate(count=Count('tags')).values('tags', 'count')
    month_counts = private_pics.annotate(month=ExtractMonth('date_created')).values('month').annotate(count=Count('id')).values('month', 'count').order_by('month')

    # Additional data for new charts
    size_by_category = private_pics.values('category', 'size').annotate(count=Count('id')).values('category', 'size', 'count').order_by('category', 'size')
    tag_distribution = private_pics.values('tags').annotate(count=Count('tags')).values('tags', 'count')
    avg_size_by_category = private_pics.values('category').annotate(avg_size=Avg('size')).values('category', 'avg_size').order_by('category')
    monthly_upload_trends = private_pics.annotate(month=ExtractMonth('date_created')).values('month').annotate(count=Count('id')).values('month', 'count').order_by('month')

    # Prepare data for new charts
    sunburst_labels = list(category_counts.values_list('category', flat=True))
    sunburst_parents = [''] * len(sunburst_labels)  # Top-level categories
    sunburst_values = list(category_counts.values_list('count', flat=True))

    pyramid_labels = sunburst_labels
    pyramid_values = sunburst_values

    funnel_labels = sunburst_labels
    funnel_values = [value * 1.1 for value in pyramid_values]  # Slightly inflated values for illustration

    stacked_area_labels = list(month_counts.values_list('month', flat=True))
    stacked_area_values = list(month_counts.values_list('count', flat=True))
    avg_images_per_user=(tag_counts)

    context = {
        'category_counts': json.dumps(list(category_counts)),
        'size_distribution': json.dumps(list(size_distribution)),
        'tag_counts': json.dumps(list(tag_counts)),
        'month_counts': json.dumps(list(month_counts)),
        'size_by_category': json.dumps(list(size_by_category)),
        'tag_distribution': json.dumps(list(tag_distribution)),
        'avg_size_by_category': json.dumps(list(avg_size_by_category)),
        'monthly_upload_trends': json.dumps(list(monthly_upload_trends)),
        'sunburst_labels': json.dumps(sunburst_labels),
        'sunburst_parents': json.dumps(sunburst_parents),
        'sunburst_values': json.dumps(sunburst_values),
        'pyramid_labels': json.dumps(pyramid_labels),
        'pyramid_values': json.dumps(pyramid_values),
        'funnel_labels': json.dumps(funnel_labels),
        'funnel_values': json.dumps(funnel_values),
        'stacked_area_labels': json.dumps(stacked_area_labels),
        'stacked_area_values': json.dumps(stacked_area_values),
        'avg_images_per_user': avg_images_per_user,
    }

    return render(request, 'private/analytics_view_private.html', context)


