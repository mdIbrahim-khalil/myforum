from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
try:
    from django.core.urlresolvers import reverse
except:
    from django.urls import reverse
from django.template.context_processors import csrf
from django_forum_app.models import Category, Forum, Topic, Post, Vote, Comment
from django_forum_app.forms import TopicForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from accounts.models import Activation, User

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings

import urllib.request
from io import StringIO
from PIL import Image

from bs4 import BeautifulSoup
import ssl
from io import BytesIO
import os , sys
import json
from notify.signals import notify

from django.contrib.contenttypes.models import ContentType

## utils ###

def parse_post(post_html):
    try:
        response_error = {'error_msg' : 'Exception occurred'}
        soup = BeautifulSoup(post_html, 'html.parser')

        if len(soup.find_all('img')) > 1 :
            msg = "Can't have more than 1 images in a single post"
            response_error['error_msg'] = msg
            raise Exception(msg)

        for img in soup.find_all('img'):
            img['class'] = 'uploadedImageClass'
            ''' img['max-width'] = '100%'            
            img['object-fit'] = 'contain'
            img['onerror'] = "this.style.display='none'"'''
        
        
        for iframe in soup.find_all('iframe'):
            iframe['sandbox'] = "allow-same-origin"      
                    
        return str(soup)

    except Exception as e:
        raise e

##############


def index(request):
    """Main listing."""
    categories = Category.objects.all().order_by('order')
    return render(request, "django_forum_app/list.html", {'categories': categories, 'user': request.user})


def feed(request):
    """Landing Page"""
    PAGE_SIZE = 5
    posts = Post.objects.all().order_by('-created')
    posts = [i for i in posts if i.upvotes >= conf_settings.FEED_MIN_UPVOTES]
    
    posts = sorted(posts, key=lambda x: x.upvotes, reverse=True)

    paginator = Paginator(posts, PAGE_SIZE)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "django_forum_app/feed.html", {'post':posts})


def fresh_feed(request):
    """Landing Page"""
    PAGE_SIZE = 5
    #  posts = Post.objects.filter(request.user.is_paid = False)
    activation = Activation.is_paid_user(request.user)
    is_user_paid = False
    posts = Post.objects.all().order_by('-created')
    if activation is not None:
        if activation.has_paid_for_current_date():
            is_user_paid = True

    # if activation is not None:
    #     if activation.has_paid_for_current_date():
    #         posts = Post.objects.all().order_by('-created')
    #         print("paid user")
    #     else:
    #         posts = Post.objects.filter(is_paid=False)
    #         print("unpaid user")
    # else:
    #     posts = Post.objects.filter(is_paid=False)
    #     print("unpaid user")

    paginator = Paginator(posts, PAGE_SIZE)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    posts = [i for i in posts if i.upvotes < conf_settings.FEED_MIN_UPVOTES]

    #user = User.objects.get(activation__id=activation_id, is_paid=True)
    return render(request, "django_forum_app/fresh_feed.html", {'posts':posts, 'is_paid_user':is_user_paid})
def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def forum(request, slug):
    """Listing of topics in a forum."""
    #top_topics = Topic.objects.filter(block_top=True, forums__slug=slug).order_by("-created")
    topics = Topic.objects.filter(forum__slug=slug).order_by("-created")
    #topics = list(top_topics) + list(topics)
    topics = list(topics)
    
    forum = get_object_or_404(Forum, slug=slug)

    paginator = Paginator(topics, 10)
    page_number = request.GET.get('page')
    topics2 = paginator.get_page(page_number)
    is_admin = request.user.is_superuser

    return render(request, "django_forum_app/forum.html", add_csrf(request, topics=topics2, forum=forum, is_admin=is_admin))


def search_topic(request):
    keyword = request.GET.get('keyword')
    topics = Topic.objects.filter(title__icontains=keyword).order_by("-created")
    topics = list(topics)

    paginator = Paginator(topics, 10)
    page_number = request.GET.get('page')
    topics = paginator.get_page(page_number)

    return render(request, "django_forum_app/search_topic.html", {'topics': topics, 'keyword':keyword })


def topic(request, slug, topic_id):
    """Listing of posts in a topic."""
    print("here in topic lists")
    PAGE_SIZE = 5
    forum = get_object_or_404(Forum, slug=slug)
    if Activation.is_paid_user(request.user):
        posts = Post.objects.filter(topic=topic_id).order_by("-created")
        print("paid user view")
    else:
        print("unpaid user view")
        posts = Post.objects.filter(topic=topic_id).filter(is_paid=False).order_by("-created")
        print(f"{len(posts)} posts")

    paginator = Paginator(posts, PAGE_SIZE)
    page_number = request.GET.get('page')
    posts2 = paginator.get_page(page_number)

    try:
        user = request.user.id
    except:
        user = None

    topic = Topic.objects.get(pk=topic_id)
    topic.sum_visits(user)

    is_admin = request.user.is_superuser

    votes = Vote.objects.all()
    return render(request, "django_forum_app/topic.html", add_csrf(request, slug=slug, forum=forum, posts=posts2, votes=votes,topic=topic, is_admin= is_admin))


@login_required
def close_topic(request, slug, topic_id):
    get_object_or_404(Forum, slug=slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.closed = True
    topic.save()
    return HttpResponseRedirect(reverse('forum:topic-detail', args=(slug, topic.id)))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_reply(request, slug, topic_id):
    try:
        msg = 'Error occurred. Please ensure you post only one photo in a post.'

        quote = request.GET.get('quote', '')
        author = request.GET.get('author', '')
        if quote:
            quote = '<blockquote>' + quote + '<footer>' + author + '</footer></blockquote>'

        forum = get_object_or_404(Forum, slug=slug)
        posts = Post.objects.filter(topic=topic_id).order_by("created").reverse()[:3]
        topic = Topic.objects.get(pk=topic_id)

        form_title = ''
        if topic.last_post(request.user):
            form_title = 'Re: ' + topic.last_post(request.user).title.replace('Re: ', '')

        default_data = {'title': form_title}
        form = PostForm(initial=default_data)

        if request.method == 'POST':
            quote = request.POST.get('quote', '')

            form = PostForm(request.POST)

            if form.is_valid():
                post = Post()
                post.topic = topic
                post.title = form.cleaned_data['title']
                post.body = quote + form.cleaned_data['body']
                post.creator = request.user
                post.user_ip = request.META['REMOTE_ADDR']
                post.body = parse_post(post.body)
                post.is_paid = form.cleaned_data['is_paid']
                post.save()
                # Get the tags associated with the post
                tags = form.cleaned_data.get('tags')
                tag_list = [tag.strip() for tag in tags.split(',')]
                post.tags.add(*tag_list)
                return HttpResponseRedirect(reverse('forum:topic-detail', args=(slug, topic.id,)))

        return render(request, 'django_forum_app/reply.html', {'form': form, 'topic': topic, 'forum': forum, 'posts': posts, 'quote': quote}) 
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return render(request, 'django_forum_app/reply.html', {'error_msg': msg,'form': form, 'topic': topic, 'forum': forum, 'posts': posts, 'quote': quote} )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def new_topic(request, slug):
    form = TopicForm()
    forum = get_object_or_404(Forum, slug=slug)

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = ''
            topic.creator = request.user
            topic.forum = forum
            topic.save()

            post = Post()
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['description']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']
            post.topic = topic
            post.save()
            return HttpResponseRedirect(reverse('forum:topic-detail', args=(slug, topic.id, )))

    return render(request, 'django_forum_app/new-topic.html', {'form': form, 'forum': forum})

@login_required
def delete_post(request, forum_slug, topic_id, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if post.creator == request.user :
            post.delete()
            return HttpResponseRedirect(reverse('django_forum_app:topic-detail', args=(forum_slug, topic_id)))
        else:
            return render(request, "django_forum_app/not_authorised.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post})
        

@csrf_exempt
def vote_object(request): 

    if request.user.is_authenticated:

        object_id = request.POST.get("object_id")
        vote_choice = request.POST.get("vote_choice")
        voter = request.user

        object_type = request.POST.get("object_type")

        if object_type == 'post':
            content_type = ContentType.objects.get_for_model(Post)
            obj = Post.objects.get(pk=object_id)
            obj_owner = obj.creator
            verb = "upvoted your post"
        elif object_type == 'comment':
            content_type = ContentType.objects.get_for_model(Comment)
            obj = Comment.objects.get(pk=object_id)
            obj_owner = obj.creator
            verb = "upvoted your comment"

        vote = Vote.objects.get_or_create(voter=voter, object_id=object_id, content_type=content_type) 
        vote = vote[0]
        vote.vote_verb = vote_choice
        vote.save()

        user_has_upvoted = (True if request.user.id in obj.upvoted_users else False)
        user_has_downvoted = (True if request.user.id in obj.downvoted_users else False)
        response_data =  {'upvotes' : obj.upvotes ,
                            'downvotes': obj.downvotes,
                            'vote_difference': obj.vote_difference,
                            'user_has_upvoted':user_has_upvoted,
                            'user_has_downvoted':user_has_downvoted}
        
        if vote_choice == 'UP':
            notify.send(voter, recipient=obj_owner, actor=request.user, target=obj,
                    verb=verb, nf_type='default')

        return HttpResponse(json.dumps(response_data),content_type="application/json")

    else:
        response_data =  {'message' : "Login Required to perform this operation"}
        return HttpResponse(json.dumps(response_data),content_type="application/json", status=401)


@login_required
def view_notificatoins(request):
    return render(request, "django_forum_app/notifications.html")


def post_detail(request, forum_slug, topic_id, pk):
    print("here")
    post = Post.objects.get(pk=pk)
    if post.is_paid and Activation.is_paid_user(request.user):
        post.body = post.body
        print("paid user view")
    else:
        print("unpaid user view")
        post.body = "Paid Post"

    form = CommentForm()
    comments = post.get_comments()
    paginator = Paginator(comments, 50)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':form, 'blank_form':form, 'comments': comments} )


@login_required
def add_comment_to_post(request, post_id):
    blank_form = CommentForm()
    post = get_object_or_404(Post, id=post_id)
    topic_id = post.topic.id
    forum_slug = post.topic.forum.slug
    comments = post.get_comments

    try:
        #msg = 'Error occurred. Please ensure you post only one photo in a comment.'

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if not(request.POST['text'].strip()):
                # Blank Body
                msg = 'Error Occurred During Adding Comment. Comment Body can to be blank.'
                return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':form, 'blank_form':blank_form,'comments': comments, 'error_msg': msg} )

            if form.is_valid():

                comment = Comment()
                comment.text = parse_post(form.cleaned_data['text'])
                comment.creator = request.user
                comment.post = post
                comment.save()
                
                # Send notification
                if request.user != post.creator:
                    verb = 'added comment on your post'
                    notify.send(request.user, recipient=post.creator, actor=request.user, target=post,
                            verb=verb, nf_type='default')
                return HttpResponseRedirect(comment.get_absolute_url())

            return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':form, 'blank_form':blank_form, 'comments': comments} )
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':form, 'blank_form':blank_form,'comments': comments, 'error_msg': msg} )

        

@login_required
def edit_comment(request, comment_id):
    form = CommentForm()
    blank_form = CommentForm()
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    topic_id = post.topic.id
    forum_slug = post.topic.forum.slug
    comments = post.get_comments

    try:
        #msg = 'Error occurred. Please ensure you post only one photo in a comment.'

        if not(request.POST['text'].strip()):
            # Blank Body
            msg = 'Error Occurred During Updating Comment. Comment Body can to be blank.'
            return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':form, 'blank_form':blank_form,'comments': comments, 'error_msg': msg} )

        if request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST.update({'text': parse_post(request.POST['text'])})
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(comment.get_absolute_url())

            return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':blank_form, 'blank_form':blank_form,'comments': comments} )
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return render(request, "django_forum_app/post_detail.html", {'forum_slug': forum_slug, 'topic_id':topic_id, 'post':post, 'user':request.user, 'form':blank_form, 'blank_form':blank_form, 'comments': comments, 'error_msg': msg} )

@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        post = comment.post

        if comment.creator == request.user:
            comment.delete()
            return HttpResponseRedirect(post.get_absolute_url())