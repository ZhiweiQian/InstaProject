from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser

# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField( #can also use models.ImageField())
            upload_to = 'static/images/profiles', #where to save uploaded images
            format = 'JPEG',
            options = {'quality':100},
            blank = True,
            null = True
            )
    
    def get_connections(self):
        #get all users followed by this user, 
        connections = UserConnection.objects.filter(creator=self) 
        #use .filter instead of .get because need to return multiple users.
        return connections #connections is a set

    def get_followers(self):
        #get all user following this user
        followers = UserConnection.objects.filter(following=self)
        return followers #followers is a set

    def is_followed_by(self, user):
        #check whether current user is followed by the parameter user
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set") 
        #A is creator, then A.friendship_creator_set returns all users followed by this creator
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")
        # B is the user being followed (following), B.friend_set returns all users following B

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model):
    author = models.ForeignKey(
            InstaUser,
            on_delete = models.CASCADE,#如果一个用户删除了账号那他所发的帖子都应该删了
            related_name = 'my_posts'
            )
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField( #can also use models.ImageField())
            upload_to = 'static/images/posts', #where to save uploaded images
            format = 'JPEG',
            options = {'quality':100},
            blank = True,
            null = True
            )
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)]) #parameter: provide an int as id
    

    
class Like(models.Model): #connect InstaUser and Post, their relationship
    #post 和 user都是外键(foreignkey),它们都指向别的model（分别指向 Post model & InstaUser model)
    post = models.ForeignKey(
            Post,
            on_delete = models.CASCADE,
            related_name = 'likes')
    """
    在某个外键下定义related_name,你就能在这个外键上通过这个name（likes）去找到所有作用于这个外键的objects。
    比如在post这个外键下定义了related_name = 'likes'. post就可以通过调用post.likes来找到所有作用于这个post的点赞  
    
    """        
    user = models.ForeignKey(
            InstaUser,
            on_delete = models.CASCADE,
            related_name = 'likes')
    """
    同理用user.likes可以找到这个user点过的所有的赞
    """
    class Meta:
        unique_together = ("post","user")
        #a (post, user) pair can only have 1 like object,某个人只能给某幅图点一次赞
    
    def __str__(self):
        return 'Like: ' + self.user.username+' likes ' + self.post.title
        
    