from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Comment
from .querysets import post_annotation
from blogicum.settings import PAGINATION
from .forms import ProfileEditForm, PostForm, CommentForm
from django.utils.timezone import now

User = get_user_model()


class PostAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostMixin(PostAuthorMixin, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        post_id = self.kwargs.get(self.pk_url_kwarg)
        return redirect(reverse(
            'blog:post_detail', kwargs={'post_id': post_id}
        ))

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username_slug': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostIndexView(ListView):
    model = Post
    form_class = PostForm
    template_name = 'blog/index.html'
    paginate_by = PAGINATION

    def get_queryset(self):
        return post_annotation(Post.objects.published())


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            Post.objects.published(),
            pk=self.kwargs['post_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATION

    def get_queryset(self):
        # Получаем категорию по slug и проверяем, что она опубликована
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username_slug']
        )

    def get_queryset(self):
        author = self.get_author()
        posts_list = post_annotation(author.posts.all())

        if self.request.user != author:
            posts_list = posts_list.filter(
                pub_date__lte=now(),
                is_published=True,
                category__is_published=True
            )

        return posts_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username_slug': self.request.user.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username_slug': self.request.user.username}
        )


class PostEditView(PostMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get(self.pk_url_kwarg)}
        )


class PostDeleteView(PostMixin, DeleteView):
    pass


class CommentCreateView(CommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.post_id = self.kwargs.get('post_id')
        form.instance.post = get_object_or_404(Post, pk=self.post_id)
        return super().form_valid(form)


class CommentUpdateView(PostAuthorMixin, CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(PostAuthorMixin, CommentMixin, DeleteView):
    pass
