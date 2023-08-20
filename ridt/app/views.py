from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegistrationForm, UserLoginForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('website-index')
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print("Someone try to login and failed")
            print(f"Username: {username} and password: {password}")
            return HttpResponse('INVALID LOGIN DETAILS')

    return render(request, 'app/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('website-index')


def user_register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():

            user = user_form.save()
            user.save()

        else:
            print(user_form.errors)
    else:
        user_form = UserRegistrationForm()

    return render(request, 'app/register.html', {'form': user_form})


@login_required
def dashboard(request):
    return render(request, 'app/home.html')


@login_required
def blog(request):
    context = {
        'posts': Blog.objects.all(),
        'title':'Blog'
    }
    return render(request, 'app/blog.html', context)


@login_required
def home(request):
    context = {
        'title':'Index'
    }
    return render(request, 'app/home.html', context)


class PostListView(ListView):
    model = Blog
    template_name = 'app/blog.html'
    context_object_name = 'posts'
    ordering = ['-create_timestamp']


class PostDetailView(DetailView):
    model = Blog

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = self.get_object()
            form.instance.created_by = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse('post-detail', kwargs={'pk':self.get_object().pk}))


    def get_context_data(self, **kwargs):
        post_comment = Comment.objects.all().filter(post=self.object.id)
        post_comment_count = Comment.objects.all().filter(post=self.object.id).count()
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comment': post_comment,
            'post_comment_count': post_comment_count,
        })
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('app-blog')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False
