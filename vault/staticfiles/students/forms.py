from .models import Notes, Ebooks, JobApplication, Assignments, Mark, DoWork, Attachments, Profile, Posts, DigitalAssets
from django import forms


class NoteForm(forms.ModelForm):
    class Meta():
        model = Notes
        fields = ['subject', 'chapter', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 15})
        }


# ebook-form
class EbookForm(forms.ModelForm):
    class Meta():
        model = Ebooks
        fields = ['subject', 'name', 'ebook']
        widgets = {
            'subject': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        def clean_ebook(self):
            ebook = self.cleaned_data.get('ebook')

            if ebook:
                if not ebook.name.endswith('.pdf'):
                    raise forms.ValidationError('Only PDF files are allowed.')
                if ebook.content_type != 'application/pdf':
                    raise forms.ValidationError('The uploaded file is not a valid PDF.')

            return ebook


# get job form

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }


# assignment form

class AssignmentsForm(forms.ModelForm):
    class Meta():
        model = Assignments
        fields = ['title', 'subject', 'attachments', 'due_on']


# mark as completed
class MarkForm(forms.ModelForm):
    class Meta():
        model = Mark
        fields = ['is_completed']


# do work
class DoWorkForm(forms.ModelForm):
    class Meta():
        model = DoWork
        fields = ['write']
        widgets = {
            'write': forms.Textarea(attrs={'class': 'form-control', 'rows': 30, 'cols': 96})
        }


# attach attachments form

class AttachmentsForm(forms.ModelForm):
    class Meta():
        model = Attachments
        fields = ['add_attachments', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'cols': 97})
        }


# profile form

class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_image']


# add post form

class PicsForm(forms.ModelForm):
    class Meta():
        model = Posts
        fields = ['pic']


# digital assets form

class DigitalAssetsForm(forms.ModelForm):
    class Meta():
        model = DigitalAssets
        fields =['asset_name','asset','type','text','thumbnail']
