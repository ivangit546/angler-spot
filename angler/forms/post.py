from django import forms 
from angler.models.post import Post, Comment

class Post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')

class PostComment(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('text')        