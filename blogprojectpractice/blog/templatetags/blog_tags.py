from blog.models import Post
from django import template

register = template.Library()

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()  

@register.inclusion_tag('blog/latest_post123.html')
def show_latest_post():
    latest_post = Post.objects.order_by('-publish')[:3]
    return {'latest_post': latest_post} #we are returning context object

from django.db.models import Count
# @register.ass
def get_most_commented_post():
    return Post.objects.annotate(total_comment=Count('comments')).order_by('-total_comment')[:4]
