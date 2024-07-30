from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pdf
from .forms import PdfForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
import os
import zipfile
from django.db.models import Count, Avg, Sum
import json
from django.http import JsonResponse

# Create your views here.

@login_required
def store_pdfs(request):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            messages.success(request, f'{pdf.name} saved to database sqlite3')
            return redirect('store_pdfs')
    else:
        form = PdfForm()
    return render(request, 'pdf/store_pdfs.html', {'form': form})


@login_required
def view_pdfs(request):
    query = request.GET.get('query', '')
    filter_type = request.GET.get('filter_type', '')

    data = Pdf.objects.filter(user=request.user)

    if query:
        data = data.filter(name__icontains=query)

    if filter_type:
        data = data.filter(type=filter_type)

    return render(request, 'pdf/view_pdfs.html', {'data': data, 'query': query, 'filter_type': filter_type})


@login_required
def delete_pdfs(request, pdf_id):
    pdf = get_object_or_404(Pdf, id=pdf_id)
    pdf.delete()
    messages.success(request, f'{pdf.name} deleted successfully')
    return redirect('view_pdfs')


@login_required
def download_all_pdfs(request):
    user_pdfs = Pdf.objects.filter(user=request.user)
    zip_filename = f"{request.user.username}_pdfs.zip"
    zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for pdf in user_pdfs:
            pdf_path = pdf.pdf.path
            pdf_filename = os.path.basename(pdf_path)
            zipf.write(pdf_path, pdf_filename)

    with open(zip_filepath, 'rb') as zipf:
        response = HttpResponse(zipf.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    os.remove(zip_filepath)  # Remove the zip file after sending it
    return response

@login_required
def pdf_analytics(request):
    pdfs = Pdf.objects.filter(user=request.user)

    # Existing data for charts
    pdf_types = list(pdfs.values('type').annotate(count=Count('type')))
    pdf_categories = list(pdfs.values('category').annotate(count=Count('category')))
    pdf_sizes = list(pdfs.values('size').annotate(count=Count('size')))
    pdf_tags = list(pdfs.values('tags').annotate(count=Count('tags')).filter(tags__isnull=False))

    # Additional data for new charts
    pdf_upload_times = list(pdfs.values('uploaded_at__date').annotate(count=Count('id')).order_by('uploaded_at__date'))
    pdf_types_detailed = list(pdfs.values('type').annotate(avg_size=Avg('size'), total_size=Sum('size')))
    pdf_category_sizes = list(pdfs.values('category').annotate(avg_size=Avg('size'), total_size=Sum('size')))

    # Aggregate data for average calculations
    avg_size_per_pdf = pdfs.aggregate(avg_size=Avg('size'))['avg_size'] or 0

    # Convert dates to strings for JSON serialization
    def convert_dates(data):
        for item in data:
            if 'uploaded_at__date' in item:
                item['uploaded_at__date'] = item['uploaded_at__date'].strftime('%Y-%m-%d')
        return data

    context = {
        'pdf_types': json.dumps(pdf_types),
        'pdf_categories': json.dumps(pdf_categories),
        'pdf_sizes': json.dumps(pdf_sizes),
        'pdf_tags': json.dumps(pdf_tags),
        'pdf_upload_times': json.dumps(convert_dates(pdf_upload_times)),
        'pdf_types_detailed': json.dumps(pdf_types_detailed),
        'pdf_category_sizes': json.dumps(pdf_category_sizes),
        'avg_size_per_pdf': avg_size_per_pdf,
    }
    return render(request, 'pdf/pdf_analytics.html', context)