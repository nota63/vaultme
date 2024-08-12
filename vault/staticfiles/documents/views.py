from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Documents
from .forms import DocumentForm
from django.contrib import messages
import os
import zipfile
from django.http import HttpResponse
from django.shortcuts import render
from .models import Documents
from django.conf import settings
from django.db.models import Count
from django.db.models import Count, Avg, Min, Max


# Create your views here.
@login_required
def store_documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, f'document {document.name} saved success')
            return redirect('store_documents')
    else:
        form = DocumentForm()
    return render(request, 'doc/store_documents.html', {'form': form})


@login_required
def view_documents(request):
    query = request.GET.get('q')
    doc_type = request.GET.get('type')
    country = request.GET.get('country')

    documents = Documents.objects.filter(user=request.user)

    if query:
        documents = documents.filter(name__icontains=query)

    if doc_type:
        documents = documents.filter(type=doc_type)

    if country:
        documents = documents.filter(country=country)

    return render(request, 'doc/view_documents.html', {'data': documents})


@login_required
def download_documents(request):
    documents = Documents.objects.filter(user=request.user)

    # Create a temporary zip file
    zip_subdir = "documents"
    zip_filename = f"{zip_subdir}.zip"

    s = HttpResponse(content_type="application/zip")
    s['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(s, "w") as zf:
        for document in documents:
            file_path = document.document.path
            file_name = os.path.basename(file_path)
            zf.write(file_path, os.path.join(zip_subdir, file_name))

    return s


@login_required
def delete_documents(request, doc_id):
    document = get_object_or_404(Documents, id=doc_id)
    document.delete()
    messages.success(request, f'document {document.name} has been deleted')
    return redirect('view_documents')


@login_required
def analytics_view_doc(request):
    documents = Documents.objects.filter(user=request.user)

    # Existing data for charts
    document_types = documents.values('type').annotate(count=Count('type'))
    document_countries = documents.values('country').annotate(count=Count('country'))
    document_legality = documents.values('is_legal').annotate(count=Count('is_legal'))

    # Additional data for new charts
    document_nominees = documents.values('nominee').annotate(count=Count('nominee'))
    document_type_doc = documents.values('type_doc').annotate(count=Count('type_doc'))

    context = {
        'document_types': list(document_types),
        'document_countries': list(document_countries),
        'document_legality': list(document_legality),
        'document_nominees': list(document_nominees),
        'document_type_doc': list(document_type_doc),
        'avg_documents_per_user':
            documents.values('user').annotate(avg_docs=Count('id')).aggregate(avg_docs=Avg('avg_docs'))['avg_docs'],
    }
    return render(request, 'doc/analytics.html', context)


def guide(request):
    return render(request,'doc/guide.html')