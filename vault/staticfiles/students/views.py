from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes, Ebooks, Job, JobApplication, Assignments, DoWork, Attachments, Profile, Posts, DigitalAssets
from .forms import NoteForm, EbookForm, JobApplicationForm, AssignmentsForm, MarkForm, DoWorkForm, AttachmentsForm, \
    ProfileForm, PicsForm, DigitalAssetsForm

from django.contrib import messages
from plyer import notification
import time
import os
from zipfile import ZipFile
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
import wikipediaapi
from googletrans import Translator
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import time
from datetime import datetime


# Create your views here.
@login_required
def create_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            try:
                note = form.save(commit=False)
                note.user = request.user
                note.save()
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            messages.success(request, f'congratulations {note.user} your note added successfully')
            time.sleep(2)
            notification.notify(
                title='VaultMe',
                message=f'Notes of {note.subject}/ chapter:{note.chapter} saved to database\n and you have used total {len(note.notes)} characters!',
                timeout=10
            )
            return redirect('create_notes')
    else:
        form = NoteForm()
    return render(request, 'students/create_notes.html', {'form': form})


@login_required
def view_notes(request):
    data = Notes.objects.filter(user=request.user)
    search = request.GET.get('search')
    if search != None:
        data = Notes.objects.filter(user=request.user, subject__icontains=search)
    return render(request, 'students/view_notes.html', {'data': data})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Notes, pk=pk, user=request.user)
    return render(request, 'students/note_detail.html', {'note': note})


@login_required
def delete_notes(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    note.delete()
    messages.success(request, f'{note.chapter} notes deleted successfully')
    return redirect('view_notes')


@login_required
def edit_note(request, pk):
    note = get_object_or_404(Notes, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f'Note {note.chapter} updated successfully')
            return redirect('view_notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'students/edit_note.html', {'form': form, 'note': note})


@login_required
def search_wikipedia(request):
    query = request.POST.get('query')
    user_agent = 'Vaultme/1.0 (http://vaultme.com; raginimms627@gmail.com)'  # Replace with your app info
    wiki_wiki = wikipediaapi.Wikipedia('en', headers={'User-Agent': user_agent})
    page = wiki_wiki.page(query)

    if page.exists():
        result = {
            'title': page.title,
            'summary': page.summary[:100000000],  # Limit summary to 1000 characters
            'full_url': page.fullurl
        }
    else:
        result = f"No data found for ''{query}'' "

    return render(request, 'students/wekipedia.html', {'result': result, 'query': query})


@login_required
def translator(request):
    translation = ''
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            translator = Translator()
            translation = translator.translate(text, src='en', dest='hi').text
    return render(request, 'students/translator.html', {'translation': translation})


@login_required
def grammar_check(request):
    spell = SpellChecker()

    if request.method == 'POST':
        text = request.POST.get('text', '')
        words = text.split()
        corrected_words = []

        for word in words:
            # Get candidates (possible corrections)
            candidates = spell.candidates(word)
            # Use the most likely correction or the original word
            corrected_word = spell.candidates(word).pop() if candidates else word
            corrected_words.append(corrected_word)

        corrected_text = ' '.join(corrected_words)

        return render(request, 'students/grammar_check.html', {
            'original_text': text,
            'corrected_text': corrected_text
        })

    return render(request, 'students/grammar_check.html')


# EBOOK STORAGE
@login_required
def store_ebooks(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                ebook = form.save(commit=False)
                ebook.user = request.user
                ebook.save()
                messages.success(request, 'Ebook saved successfully')
                notification.notify(
                    title='VaultMe',
                    message=f'Congratulations {ebook.user.username}, your ebook was saved successfully! You can '
                            f'access it later.',
                    timeout=6
                )
                return JsonResponse({'success': True}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        data = Ebooks.objects.filter(user=request.user)
        form = EbookForm()
        search = request.GET.get('search')
        if search != None:
            data = Ebooks.objects.filter(user=request.user, name__icontains=search)
        return render(request, 'students/store_ebooks.html', {'form': form, 'data': data})


@login_required
def ebook_detail(request, pk):
    data = get_object_or_404(Ebooks, pk=pk, user=request.user)
    return render(request, 'students/ebook_detail.html', {'data': data})


@login_required
def delete_ebooks(request, ebook_id):
    data = get_object_or_404(Ebooks, id=ebook_id)
    data.delete()
    messages.success(request, f'{data.ebook} deleted successfully')
    notification.notify(
        title='VaultMe',
        message=f'{data.ebook} deleted successfully, thank you for using our platform for..',
        timeout=5
    )
    return redirect('store_ebooks')


@login_required
def career_recommendation_view(request):
    # Sample dataset
    data = {
        'career': [
            'Data Scientist', 'Software Developer', 'Mechanical Engineer',
            'Civil Engineer', 'Digital Marketer', 'Data Analyst', 'Product Manager'
        ],
        'skills': [
            'Python, Machine Learning, Statistics, Data Analysis',
            'Java, C++, Problem Solving, Software Development',
            'Mechanics, CAD, Problem Solving, Engineering Principles',
            'Construction, CAD, Project Management, Engineering Principles',
            'SEO, Content Creation, Social Media, Marketing Strategy',
            'SQL, Data Analysis, Statistics, Excel',
            'Product Management, Agile, Scrum, Leadership'
        ],
        'description': [
            'Data Scientists analyze and interpret complex data to help companies make decisions.',
            'Software Developers create and maintain software applications.',
            'Mechanical Engineers design, develop, and test mechanical systems and devices.',
            'Civil Engineers plan, design, and oversee construction and maintenance of building structures and '
            'infrastructure.',
            'Digital Marketers promote products and services through digital channels.',
            'Data Analysts collect, process, and perform statistical analyses on data.',
            'Product Managers oversee the development and delivery of products from inception to launch.'
        ],
        'average_salary': [
            '$120,000', '$100,000', '$85,000', '$80,000', '$70,000', '$65,000', '$110,000'
        ],
        'growth_prospects': [
            'High', 'High', 'Moderate', 'Moderate', 'High', 'High', 'High'
        ]
    }

    df = pd.DataFrame(data)

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['skills'])

    recommended_careers = []

    if request.method == 'POST':
        student_skills = request.POST.get('skills')

        # Check if student_skills is not empty
        if student_skills:
            # Recommend careers based on skills
            student_tfidf = tfidf.transform([student_skills])
            cosine_sim_student = linear_kernel(student_tfidf, tfidf_matrix)
            sim_scores = list(enumerate(cosine_sim_student[0]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            recommended_indices = [i[0] for i in sim_scores if i[1] > 0.1]  # Filter by similarity threshold
            recommended_careers = df.iloc[recommended_indices].to_dict('records')

    return render(request, 'students/career_recommendation.html', {'recommended_careers': recommended_careers})


# display job postings

@login_required
def job_posting(request):
    jobs = Job.objects.all()
    search = request.GET.get('search')
    if search != None:
        jobs = Job.objects.filter(skills_required__icontains=search)
    return render(request, 'students/job_posting.html', {'jobs': jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'students/job_detail.html', {'job': job})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.job = job
                application.user = request.user
                application.save()
            except Exception as e:
                return JsonResponse({str(e)}, status=400)
        messages.success(request, f'successfully applied')
        notification.notify(
            title='VaultMe',
            message=f'successfully applied for job {job.title}! Company will get in touch with you shortly\n have a '
                    f'great day ahead!!',
            timeout=7
        )

        return redirect('career_recommendation')
    else:
        form = JobApplicationForm()
    return render(request, 'students/apply_job.html', {'form': form})


@login_required
def applied_jobs(request):
    data = JobApplication.objects.filter(user=request.user)
    return render(request, 'students/applied_jobs.html', {'data': data})


# HOMEWORK SECTION
@login_required
def add_assignments(request):
    if request.method == 'POST':
        form = AssignmentsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                assignment = form.save(commit=False)
                assignment.user = request.user
                assignment.save()
                due_on = form.cleaned_data['due_on']
                current_date = datetime.now().date()
                if due_on == current_date:
                    notification.notify(
                        title='VaultMe',
                        message='same day!',
                        timeout=5
                    )
            except Exception as e:
                return JsonResponse(
                    {'message': str(e)}
                )
            messages.success(request, f'Homework/assignment {assignment.title} listed to pending work..\n ')
            notification.notify(
                title='VaultMe',
                message=f'Your assignment {assignment.title} is due on {assignment.due_on} dont forget to complete it '
                        f'before {assignment.due_on}!',
                timeout=5
            )
            return redirect('add_assignments')
    else:
        form = AssignmentsForm()
    data = Assignments.objects.filter(user=request.user)
    search = request.GET.get('search')
    if search != None:
        data = Assignments.objects.filter(user=request.user, title__icontains=search)
    return render(request, 'students/add_assignment.html', {'form': form, 'data': data})


@login_required
def mark(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MarkForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f'{assignment} status changed successfully')
            notification.notify(
                title='VaultMe',
                message=f'Assignment {assignment} status changed successfully',
                timeout=4
            )
            return redirect('add_assignments')
    else:
        form = MarkForm(instance=assignment)
    return render(request, 'students/mark.html', {'form': form, 'assignment': assignment})


@login_required
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk, user=request.user)
    try:
        assignment.delete()
    except Exception as e:
        return JsonResponse(
            {'message': str(e)}
        )

    messages.success(request, f'Assignment {assignment} deleted successfully')
    notification.notify(
        title='VaultMe',
        message=f'{assignment} was deleted!',
        timeout=5
    )
    return redirect('add_assignments')


@login_required
def edit_assignments(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentsForm(request.POST, instance=assignment)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                return JsonResponse(
                    {'message': str(e)}

                )
            messages.success(request, f'{assignment} updated successfully')
            return redirect('add_assignments')
    else:
        form = AssignmentsForm(instance=assignment)
    return render(request, 'students/edit_assignments.html', {'form': form, 'assignment': assignment})


@login_required
def do_work(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DoWorkForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            write = form.cleaned_data['write']
            do_work_instance = DoWork(write=write, user=request.user,
                                      assignment=assignment)  # Assuming DoWork has 'user' and 'assignment' fields
            do_work_instance.save()
            messages.success(request, f'Homework {assignment} has been written successfully')
            return redirect('add_assignments')

    else:
        form = DoWorkForm(instance=assignment)
    data = DoWork.objects.filter(assignment=assignment)
    return render(request, 'students/do_work.html', {'form': form, 'assignment': assignment, 'data': data})


@login_required
def attachments(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AttachmentsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                add_attachments = form.cleaned_data['add_attachments']
                description = form.cleaned_data['description']
                attachments_instance = Attachments(add_attachments=add_attachments, description=description,
                                                   assignment=assignment, user=request.user)
                attachments_instance.save()
                messages.success(request, f'Attachments attached to {assignment} successfully')
                return redirect('add_assignments')
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
    else:
        form = AttachmentsForm()
    data = Attachments.objects.filter(assignment=assignment)
    return render(request, 'students/attachments.html', {'form': form, 'assignment': assignment, 'data': data})


@login_required
def set_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
            messages.success(request, 'Profile updated successfully')
            notification.notify(
                title='VaultMe',
                message=f'Hello {profile.user} welcome to VaultMe\n we are glad you joined us thank you\n have a great day🙂',
                timeout=5
            )
            return redirect('browse_profile')
    else:
        form = ProfileForm()
    return render(request, 'students/set_profile.html', {'form': form})


@login_required
def browse_profile(request):
    profile = Profile.objects.filter(user=request.user)
    data = Posts.objects.filter(user=request.user)
    return render(request, 'students/browse_profile.html', {'profiles': profile, 'data': data})


@login_required
def post(request):
    if request.method == 'POST':
        form = PicsForm(request.POST, request.FILES)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.user = request.user
            posts.save()
            time.sleep(2)
            messages.success(request, 'success..')
            return redirect('browse_profile')
    else:
        form = PicsForm()
    return render(request, 'students/post.html', {'form': form})


@login_required
def manage_posts(request):
    data = Posts.objects.filter(user=request.user)
    search = request.GET.get('search')
    if search != None:
        data = Posts.objects.filter(user=request.user, date__icontains=search)
    return render(request, 'students/manage_posts.html', {'data': data})


@login_required
def delete_posts(request, pk):
    posts = get_object_or_404(Posts, pk=pk, user=request.user)
    posts.delete()
    messages.success(request, 'your post has been deleted')
    return redirect('manage_posts')


@login_required
def download_all_images(request):
    posts = Posts.objects.filter(user=request.user)
    zip_filename = "all_images.zip"
    zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with ZipFile(zip_file_path, 'w') as zip_file:
        for post in posts:
            if post.pic:
                file_path = post.pic.path
                zip_file.write(file_path, os.path.basename(file_path))

    response = HttpResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    return response


# all students

@login_required
def all_students(request):
    students = Profile.objects.all()
    return render(request, 'students/all_students.html', {'students': students})


@login_required
def user_profile(request, pk):
    student = get_object_or_404(Profile, pk=pk)
    posts = Posts.objects.filter(user=student.user)  # Assuming Posts has a ForeignKey to the user
    return render(request, 'students/user_profile.html', {'student': student, 'posts': posts})


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('browse_profile')  # Redirect to profile view after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'students/edit_profile.html', {'form': form})


# DIGITAL ASSETS SECTION
@login_required
def assets(request):
    if request.method == 'POST':
        form = DigitalAssetsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                asset = form.save(commit=False)
                asset.user = request.user
                asset.save()
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
            messages.success(request, f'{asset.asset_name} saved to cloud')
            return redirect('assets')
    else:
        form = DigitalAssetsForm()
    data = DigitalAssets.objects.filter(user=request.user)
    return render(request, 'students/assets.html', {'form': form, 'data': data})


@login_required
def delete_assets(request, pk):
    asset = get_object_or_404(DigitalAssets, pk=pk, user=request.user)
    asset.delete()
    messages.success(request, f"{asset.asset_name} deleted successfully")
    return redirect('assets')


@login_required
def edit_assets(request, pk):
    asset = get_object_or_404(DigitalAssets, pk=pk)
    if request.method == 'POST':
        form = DigitalAssetsForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, f'{asset.asset_name} updated successfully')
            return redirect('assets')
    else:
        form = DigitalAssetsForm(instance=asset)
    return render(request, 'students/edit_assets.html', {'form': form, 'asset': asset})
