from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from InstaApp.models import Post, Like, InstaUser, UserConnection
from InstaApp.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HelloWorld(TemplateView):
    template_name = 'test.html'
    
class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    
    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__' #all fields in model
    login_url = 'login'
    
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")
    #use reverse_lazy instead of reverse when doing delete. otherwise will cause "circular import" error. 
    #meaning you start jumping to another link when delete is still in progress, which is not allowed in Django
class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

    
@ajax_request#the function addLike() is used to reponse to ajax request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user) #create a models.Like object
        like.save()#save the like object into database
        #if this (post, user) pair already have a like relationship, because we defined unique_together under Like, 
        #this will throw an error, will be handled by Exception.
        result = 1
    except Exception as e:#if a user already liked a post, then click the like icon again, that means unlike the post
        like = Like.objects.get(post=post, user=request.user)
        like.delete()#delete this like object from database
        result = 0

    return {#jason format
        'result': result,
        'post_pk': post_pk
    }    