from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import PostCreateForm, PostUpdateForm

from django.db.models import Q


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def tag_find(request):
	tag = '#' + request.GET['q']
	posts = Post.objects.filter(Q(title__icontains=tag)|Q(content__icontains=tag))
	total_posts = len(posts)
	params = {'posts':posts, 'tag':tag, 'lenpost':total_posts}

	return render(request, 'blog/search.html', params)

def search(request):
	query = request.GET['q']
	posts = Post.objects.filter(Q(title__icontains=query)|Q(content__icontains=query))
	total_posts = len(posts)
	params = {'posts':posts, 'tag':query, 'lenpost':total_posts}

	return render(request, 'blog/search.html', params)

class PostDetailView(DetailView):
    model = Post

def PostCreateView(request):
	context = {}

	if not request.user.is_authenticated:
		return redirect('login')

	form = PostCreateForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.instance.author = request.user
		form.save()

		form = PostCreateForm()

	context['form'] = form

	return render(request, "blog/post_form.html", context)

# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

def PostUpdateView(request, pk):
	context = {}

	if not request.user.is_authenticated:
		return redirect('login')

	blog = get_object_or_404(Post, id=pk)

	if request.POST:
		form = PostUpdateForm(request.POST or None, request.FILES or None, instance=blog)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog = obj

	form = PostUpdateForm(
		initial={
			"title": blog.title,
			"content": blog.content,
			"image": blog.image
		}
	)

	context['form'] = form
	return render(request, 'blog/post_edit.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
