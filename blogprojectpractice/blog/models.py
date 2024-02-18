from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

from taggit.managers import TaggableManager
class Post(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length =225)
    slug = models.SlugField(max_length=264, unique_for_date='publish')
    author = models.ForeignKey(User,related_name ='blog_posts',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created= models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length= 10, choices=STATUS_CHOICES,default= 'draft')
    objects = CustomManager()
    # This manager handle the tags 
    # how ? : Post.tags.all(): it return all th tags associated with the post
    tags= TaggableManager()


    class Meta:
        # when we use query post.object.all() it will come in order 
        # we don't need to use order by
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'), self.slug])
    

# Model related to comments Section
# multiple Comments we get for single post: Many to One Relation
    # we can use ForeignKey for Many to One
class Comments(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    # while query we get post object, and now i want to know all the Comments
    # related to this post
    # post.comments (related_name='comments')
    name = models.CharField(max_length=32)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # sometime we have to hide unneccessary Comments
    active = models.BooleanField(default=True)

    # we want letest comment first
    class Meta:
        ordering = ('-created',)

    # if any person trying to disply comment object return
    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)
