from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog_list')

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog_list')

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
