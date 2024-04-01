from django import forms
from .models import Post ,Comment

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
 
class CommentCreateForm(forms.ModelForm):
    """コメントフォーム"""

    class Meta:
        model = Comment
        exclude = ('target', 'created_at')