from django.shortcuts import render,get_object_or_404
from blog.models import Post
from taggit.models import Tag
from blog import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
# Create your views here.


@login_required
def PostListView(request,tag_slug=None):
    # post_list = Post.objects.all()
    # In the main page , we want only published post not Draft 
    # let create one model Manager
    post_list = Post.objects.all()

    # tag functionality
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    # let create pagination to display records
    paginator = Paginator(post_list,2) #how many page you want
    page_number =request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage: #last page
        post_list=paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html', {'post_list':post_list,'tag':tag})

# if we do same thing using CBV
from django.views.generic import ListView

@login_required
class PostListViewCBV(ListView):
    model =  Post
    paginate_by = 2
    # it automatically take page_list.html 

from blog.forms import CommentForm

@login_required
def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # requirement is add comments detail page 
    # get only active column
    comments = post.comments.filter(active=True)
    csubmit=False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # end-user only provide name, email and body,other things we get 
            new_comment =form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    # if not a post request , just display the form 
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form':form,'csubmit':csubmit,'comments':comments})

# To send send_mail
from django.core.mail import send_mail
from blog.forms import EmailSendForm

@login_required
def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    if request.method == 'POST':
        form= EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({}) recommended you to read"{}"'.format(cd['name'],cd['email'],post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read Post at:\n {}\n\n{}\'s Comments:\n{}'.format(post_url, cd['name'],cd['comments'])
            send_mail(subject,message,'durga@blog.com',[cd['to']])
            sent = True
    else:
        form = EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form': form,'post': post, 'sent':sent})

# user view define here 
def logout_view(request):
    return render(request, 'blog/logout.html')


def signup_views(request):
    #get
    form = forms.SignUpForm()
    #post
    if request.method =='POST':
        form = forms.SignUpForm(request.POST)
        user = form.save()
        user.set_password(user.password)
        user.save()
        return HttpResponseRedirect('/accounts/login')
    return render(request, 'blog/signup.html', {'form': form})
