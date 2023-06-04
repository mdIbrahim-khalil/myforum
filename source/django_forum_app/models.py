from django.db import models
from django.conf import settings
from photologue.models import Photo
from django.utils.translation import ugettext_lazy as _
try:
    User = settings.AUTH_USER_MODEL
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User

#from vote.models import VoteModel

from django.conf import settings as conf_settings
from django_forum_app.templatetags import forum_tags
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import Activation

from flag.models import Flag

from django.urls import reverse

from bs4 import BeautifulSoup
from taggit.managers import TaggableManager

POSTS_PER_PAGE = getattr(settings, 'POSTS_PER_PAGE', 10)

class Category(models.Model):
    order = models.IntegerField()
    title = models.CharField(max_length=60)

    def get_forums(self):
        return Forum.objects.filter(category=self.id)

    def __str__(self):
        return self.title


class Forum(models.Model):
    title = models.CharField(max_length=60)
    slug = slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_summary(self):
        if len(self.description) > 50:
            return self.description[:50] + '...'
        return self.description

    def get_visits(self):
        vs = 0
        for t in self.topic_set.all():
            vs += t.visits
        return vs

    def has_seen(self, user=None):
        if user.is_authenticated():
            for t in self.topic_set.all():
                if not t.has_seen(user):
                    return False
        return True

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])

    def num_topics(self):
        return self.topic_set.all().count()

    def last_post(self, user):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_post(user)
                if l:
                    if not last:
                        last = l
                    elif l.created > last.created:
                        last = l
            return last
    
    def get_absolute_url(self):
        return reverse('django_forum_app:forum-detail', args=[str(self.slug)])

class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    # forums = models.ManyToManyField(Forum)
    block_top = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)
    visits = models.IntegerField(default=0)
    user_lst = models.TextField(blank=True, null=True)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self, user):
        print("pre postset")
        if self.post_set.count():
            print("post postset")
            if Activation.check_paid_user(user):
                print("pre check paid user")
                return self.post_set.order_by("-created")[0]
            else:
                print("non paid user")
                return self.post_set.filter(is_paid=False).order_by("-created").first()

    def sum_visits(self, user_id=None):
        if user_id:
            if self.user_lst:
                lst = self.user_lst.split(',')
                if str(user_id) not in lst:
                    self.user_lst += ',' + str(user_id)
            else:
                self.user_lst = str(user_id)
        self.visits += 1
        self.save()

    def has_seen(self, user=None):
        if user.is_authenticated():
            if self.user_lst:
                lst = self.user_lst.split(',')
                if str(user.id) in lst:
                    return True
            return False
        return True

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse('django_forum_app:topic-detail', args=[self.forum.slug, self.id])

VOTE_OPTIONS = [('UP','UP')
                ,('DOWN', 'DOWN')
                ,('NONE', 'NONE')]

class Vote(models.Model):
    vote_verb = models.CharField(choices =VOTE_OPTIONS, default='NONE', max_length=10)
    voter = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_votes", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    content_object=GenericForeignKey('content_type', 'object_id')

class Post(models.Model):
    title = models.CharField(max_length=60, verbose_name=_("Title"))
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_posts", on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    body = models.TextField(max_length=10000)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    telegram_id = models.CharField(max_length=20, blank=True, null=True)
    # Add the tags field
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", through=None, blank=False)
    is_paid = models.BooleanField(default=False)
    #user_typ = models.ForeignKey(Activation, limit_choices_to={'is_paid': True}, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)

    flags = GenericRelation(Flag)
    votes = GenericRelation(Vote)

    def __str__(self):
        return str(self.title)

    def get_post_num(self):
        return Post.objects.filter(topic__id=self.topic_id).filter(created__lt=self.created).count()

    def get_page(self):
        return self.get_post_num() / POSTS_PER_PAGE + 1

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%Y-%m-%d %H:%M"))

    def supershort(self):
        return u"%s: %s" % (self.creator, self.created.strftime("%Y-%m-%d %H:%M"))

    def get_absolute_url(self):
        return reverse('django_forum_app:post-detail', args=(self.topic.forum.slug , self.topic.id ,self.id))

    def save(self, *args, **kwargs):
        self.topic.user_lst = str(self.creator.id)
        self.topic.save()
        super(Post, self).save(*args, **kwargs)

    short.allow_tags = True

    def _get_up_votes(self):
        "Returns count of upvotes for the post."
        return self.votes.filter(vote_verb='UP').count()
    upvotes = property(_get_up_votes)

    def _get_down_votes(self):
        "Returns count of downvotes for the post."
        return self.votes.filter(vote_verb='DOWN').count()
    downvotes = property(_get_down_votes)

    def _upvoted_users(self):
        "Returns list of users whom have upvoted the post."
        voters = self.votes.filter(vote_verb='UP').values_list('voter', flat=True)
        voters = list(voters)
        return voters
    upvoted_users = property(_upvoted_users)

    def _downvoted_users(self):
        "Returns list of users whom have downvoted the post."
        voters = self.votes.filter(vote_verb='DOWN').values_list('voter', flat=True)
        voters = list(voters)
        return voters
    downvoted_users = property(_downvoted_users)

    def _flag_counts(self): 
        "Returns number of flags resgiterd for the post."
        if (self.flags.all()):
            post_flags = self.flags.all()[0].flags.all().count()
            return post_flags
        else:
            return 0
    flag_counts = property(_flag_counts)

    def _is_flagged(self):
        "Returns True if post is flagged"
        if (self.flag_counts > conf_settings.FLAGS_ALLOWED):
            return True
        else:
            return False
    is_flagged = property(_is_flagged)
    
    @property
    def vote_difference(self):
        return self.upvotes - self.downvotes


    def get_comments(self):
        return Comment.objects.filter(post=self.id).order_by("-created")


class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word

class Comment(models.Model):
    text = models.CharField(max_length=10000, verbose_name=_("Text"))
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="%(class)s_comments", on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    flags = GenericRelation(Flag)
    votes = GenericRelation(Vote)

    def _get_up_votes(self):
        "Returns count of upvotes for the comment."
        return self.votes.filter(vote_verb='UP').count()
    upvotes = property(_get_up_votes)

    def _get_down_votes(self):
        "Returns count of downvotes for the comment."
        return self.votes.filter(vote_verb='DOWN').count()
    downvotes = property(_get_down_votes)

    def _upvoted_users(self):
        "Returns list of users whom have upvoted the comment."
        voters = self.votes.filter(vote_verb='UP').values_list('voter', flat=True)
        voters = list(voters)
        return voters
    upvoted_users = property(_upvoted_users)

    def _downvoted_users(self):
        "Returns list of users whom have downvoted the comment."
        voters = self.votes.filter(vote_verb='DOWN').values_list('voter', flat=True)
        voters = list(voters)
        return voters
    downvoted_users = property(_downvoted_users)

    def get_absolute_url(self):
        return reverse('django_forum_app:post-detail', args=(self.post.topic.forum.slug , self.post.topic.id , self.post.id)) + f'#c{self.id}'
    
    def _flag_counts(self):
        "Returns number of flags resgiterd for the comment."
        if (self.flags.all()):
            post_flags = self.flags.all()[0].flags.all().count()
            return post_flags
        else:
            return 0
    flag_counts = property(_flag_counts)

    def _is_flagged(self):
        "Returns True if comment is flagged"
        if (self.flag_counts > conf_settings.FLAGS_ALLOWED):
            return True
        else:
            return False
    is_flagged = property(_is_flagged)

    def __str__(self):
        raw_html = self.text
        cleantext = BeautifulSoup(raw_html, "lxml").text
        return cleantext[0:20]
