from django import forms
from .models import Reviews, Collaborate, Projects, ProjectShare, Reply_dev, Comment_dev,Skills


# review form
class ReviewForm(forms.ModelForm):
    class Meta():
        model = Reviews
        fields = ['pros', 'cons', 'suggestion', 'image']
        widgets = {
            'pros': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'cons': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'suggestion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }


# collaborate form

class CollaborateForm(forms.ModelForm):
    class Meta():
        model = Collaborate
        fields = ['name', 'contact', 'email', 'specialized_skills', 'resume', 'applying_for']
        widgets = {
            'contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specialized_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


# projects form
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name', 'requirements', 'what_does', 'files']
        widgets = {
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'what_does': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }


# project share form

class ProjectShareForm(forms.ModelForm):
    class Meta():
        model=ProjectShare
        fields=['name','description','image','live_link']
        widgets={
            'name':forms.Textarea(attrs={'class':'form-control','rows':5}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':10}),
            'live_link':forms.Textarea(attrs={'class':'form-control','rows':4})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_dev
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply_dev
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a reply...'}),
        }



# skills form

class SkillsForm(forms.ModelForm):
    class Meta():
        model=Skills
        fields=['skill_name','image']
        widgets={
            'skill_name':forms.Textarea(attrs={'class':'form-control','rows':3})
        }



