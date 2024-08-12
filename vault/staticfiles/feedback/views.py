from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feed_done')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})


def feed_done(request):
    return render(request, 'feedback/feed_done.html')