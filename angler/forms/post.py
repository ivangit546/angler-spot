from django import forms 
from angler.models.post import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','image')

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('text',)            
        widgets = {
            'text': forms.Textarea(attrs={'placeholder':'Enter your reply here...'})
        }
        labels = {
            'text':''
        }