from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
#redirect ke login page pas mau create Post dan semacam cuma user yang punya postnya sendiri yang bisa ubah postnya

def home(request):
    return render(request, 'blog/home.html')

@login_required()
def comments(request):
    # Dictionary
    context = {
            'posts':Post.objects.all()
     }
    return render(request, 'blog/comments.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/comments.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # ini buat post diurutkan dari yang terbaru ke terlama
    paginate_by = 10 # pembatasan buat pagination, 1 page cuma ada x post aja gitu


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10 # pembatasan buat pagination, 1 page cuma ada x post aja gitu

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# secara default class di atas dan dibawah bakal search ke <app>/<model>_<viewtype>.html kalau gk di set
# yaitu blog/Post_apalah.html

class PostDetailView(DetailView):
    model = Post


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # harus login dan harus owner dri post itu
    model = Post
    success_url = '/comments/'

    def test_func(self): # biar orang gak bisa update post orang lain
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False





class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # biar setiap kali kita post, dia tau bahwa authornya yang lgi login currently
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # biar setiap kali kita post, dia tau bahwa authornya yang lgi login currently
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): # biar orang gak bisa update post orang lain
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'blog/about.html')


def burung(request):
    return render(request, 'blog/burung.html')


def makanan(request):
    return render(request, 'blog/makan.html')


def comsoon(request):
    return render(request, 'blog/whin.html')
