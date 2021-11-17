from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content','image']

class PostUpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content','image']
	
	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.content = self.cleaned_data['content']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		
		return blog_post