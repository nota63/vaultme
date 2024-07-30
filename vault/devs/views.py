from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Reviews, Collaborate, Projects, CodeSnippet, ProjectShare, Comment_dev, Reply_dev,Skills
from .forms import ReviewForm, CollaborateForm, ProjectsForm, ProjectShareForm, CommentForm, ReplyForm,SkillsForm
from django.contrib import messages
import time
from plyer import notification
from django.http import HttpResponse, JsonResponse
import logging
from django.db.models import Count, Avg, Q
import subprocess
import json
from django.middleware.csrf import get_token
import sys
import io
import contextlib
import pyjokes
import pywhatkit as kit


# Create your views here.
@login_required
def reviews(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'review submitted you can view in community')
            time.sleep(3)
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'devs/reviews.html', {"form": form})


@login_required
def view_reviews(request):
    data = Reviews.objects.all()
    return render(request, 'devs/view_reviews.html', {'data': data})


@login_required
def collaborate(request):
    if request.method == 'POST':
        form = CollaborateForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'redirecting.. ')
            time.sleep(3)
            notification.notify(
                title='VaultMe',
                message=f'Thank you {resume.user} for your interest, your application is now applying....Have a '
                        f'good day 🙂',
                timeout=8

            )

            return render(request, 'devs/success.html')
    else:
        form = CollaborateForm()
    return render(request, 'devs/collaborate.html', {'form': form})


@login_required
def success(request):
    return render(request, 'devs/success.html')


# Configure logging
logger = logging.getLogger(__name__)


@login_required
def projects(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                project = form.save(commit=False)
                project.user = request.user
                project.save()
                messages.success(request, 'Project uploaded successfully')
                return redirect('projects')
            except Exception as e:
                logger.error(f'Error uploading files: {e}')
                messages.error(request, f'Error uploading files: {e}')
    else:
        form = ProjectsForm()
    return render(request, 'devs/projects.html', {'form': form})


@login_required
def view_projects(request):
    search_query = request.GET.get('search', '')
    filter_option = request.GET.get('filter', '')

    projects = Projects.objects.filter(user=request.user)

    if search_query:
        projects = projects.filter(project_name__icontains=search_query)

    if filter_option == 'latest':
        projects = projects.order_by('-date_added')
    elif filter_option == 'oldest':
        projects = projects.order_by('date_added')

    return render(request, 'devs/view_projects.html', {'data': projects})


@login_required
def delete_projects(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    project.delete()
    messages.success(request, 'Removed project from SQLite3 engine')
    return redirect('view_projects')


@login_required
def analytics_view_projects(request):
    user = request.user

    total_projects = Projects.objects.filter(user=user).count()
    requirements_distribution = Projects.objects.filter(user=user).values('requirements').annotate(
        count=Count('requirements'))
    what_does_distribution = Projects.objects.filter(user=user).values('what_does').annotate(count=Count('what_does'))
    recent_projects = Projects.objects.filter(user=user).order_by('-date_added')[:10]
    average_projects = Projects.objects.filter(user=user).aggregate(avg_projects=Avg('id'))
    top_projects = Projects.objects.filter(user=user).values('project_name').annotate(
        count=Count('project_name')).order_by('-count')[:5]
    trends_over_time = Projects.objects.filter(user=user).annotate(month=ExtractMonth('date_added')).values(
        'month').annotate(value=Count('id')).order_by('month')

    context = {
        'total_projects': total_projects,
        'requirements_distribution': requirements_distribution,
        'what_does_distribution': what_does_distribution,
        'recent_projects': recent_projects,
        'average_projects': average_projects,
        'top_projects': top_projects,
        'trends_over_time': trends_over_time
    }

    return render(request, 'devs/analytics_view_projects.html', context)


# for code editor
@csrf_exempt
def code_editor(request):
    if request.method == 'GET':
        context = {'csrf_token': get_token(request)}
        return render(request, 'devs/code_editor.html', context)
    elif request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '')

        # Redirect stdout and stderr to capture output
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                exec(code, {}, {})
            output = buffer.getvalue()
        except Exception as e:
            output = str(e)

        return JsonResponse({'output': output})


# conversation area starts
@login_required
def share(request):
    if request.method == 'POST':
        form = ProjectShareForm(request.POST, request.FILES)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.user = request.user
            projects.save()
            messages.success(request, f'{projects.name} saved to SQLite3')
            return redirect('share')
    else:
        form = ProjectShareForm()
    return render(request, 'devs/share.html', {'form': form})


@login_required
def view_shares(request):
    data = ProjectShare.objects.all()
    if request.method == 'GET':
        search = request.GET.get('search')
        if search != None:
            data = ProjectShare.objects.filter(name__icontains=search)
    return render(request, 'devs/view_shares.html', {'data': data})


@login_required
def delete_project_share(request, pk):
    project_share = get_object_or_404(ProjectShare, pk=pk)

    # Check if the logged-in user is the owner of the project
    if project_share.user == request.user:
        project_share.delete()
        messages.success(request, 'Project share deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this project.')

    return redirect('view_shares')


@login_required
def add_comment(request, pk):
    project = get_object_or_404(ProjectShare, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect('view_shares')
    else:
        form = CommentForm()
    return render(request, 'devs/add_comment.html', {'form': form, 'project': project})


@login_required
def add_reply(request, comment_pk):
    comment = get_object_or_404(Comment_dev, pk=comment_pk)
    project = comment.project
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('view_shares')
    else:
        form = ReplyForm()
    return render(request, 'devs/add_reply.html', {'form': form, 'project': project, 'comment': comment})


@login_required
def own_projects(request):
    data = ProjectShare.objects.filter(user=request.user)
    if request.method == 'GET':
        own_search=request.GET.get('own_search')
        if own_search!=None:
            data=ProjectShare.objects.filter(name__icontains=own_search)
    return render(request, 'devs/own_projects.html', {'data': data})


@login_required
def delete_own(request, projects2_id):
    projects5 = get_object_or_404(ProjectShare, id=projects2_id)
    projects5.delete()
    messages.success(request, f'{projects5.name} has been deleted')
    return redirect('own_projects')

@login_required
def pyjokes_view(request):
    try:
        joke = pyjokes.get_joke(category='all')
    except pyjokes.pyjokes.CategoryNotFoundError:
        joke = "No jokes available in this category."
    return render(request, 'devs/pyjokes.html', {'joke': joke})

@login_required
def invite(request):
    if request.method == 'POST':
        number=request.POST.get('number')
        invite_msg=(f"Hey i am enjoying this website alot😛!\n here we can do many things such as we can store our "
                    f"data ,documents,pdfs,images,private images and many more and you know\n it has a saperate "
                    f"functions for developer i hope you will enjoy \n please click the following link and join me\n "
                    f"also the website has advanced secure and powered by django\n lets secure together\n "
                    f"https://www.vaultme.vercel.app")
        notification.notify(
            title='VaultMe',
            message=f"programme will initialize to invite {number} in 4 seconds..",

            timeout=5
        )
        time.sleep(3)
        kit.sendwhatmsg_instantly(number,invite_msg)
        return redirect('invite')
    return render(request,'devs/invite.html')

