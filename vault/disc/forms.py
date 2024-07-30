from django import forms
from .models import Blog, Comment, Reply


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user', 'title', 'description', 'image', 'url', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'url': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 5})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control','rows':1})
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control','rows':1})
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')