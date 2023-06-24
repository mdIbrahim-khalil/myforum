from django import template
from django.utils.safestring import mark_safe
import bleach
import timeago
import datetime
import django_forum_app.models
from django.conf import settings as conf_settings
from collections import Counter

register = template.Library()

_ALLOWED_ATTRIBUTES = {
        'img': ['src', 'class', 'style', 'width','height','object-fit','onerror'],
        'table': ['class'],
        'span' : ['class', 'style'],
        'iframe':['src','width','height','allowfullscreen'],
        'a':['href','rel' , 'target','title'],
        'video': ['controls','height','width'],
        'source': ['src'],
        'div' : ['class','style','dir']

}
_ALLOWED_TAGS = ['b', 'i', 'ul', 'li', 'p', 'br', 'h1', 'h2', 'h3', 'h4', 'ol', 'img', 'strong', 'code', 'em', 'blockquote',
    'table', 'thead', 'tr', 'td', 'tbody', 'th','span','iframe','a','video','source','div']


@register.filter
def check_seen(obj, user):
    return obj.has_seen(user)

@register.filter()
def safer(text):
    safer_txt = mark_safe(bleach.clean(text, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRIBUTES))
    return safer_txt

@register.filter()
def safer_with_span(text):
    return mark_safe(f'<span>{bleach.clean(text, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRIBUTES)}</span>')

@register.simple_tag
def convert_to_time_ago(date_time):
    now = datetime.datetime.now()
    tago = timeago.format(date_time, now)
    return tago

@register.simple_tag
def get_popular_forums():
    forums = django_forum_app.models.Forum.objects.all().order_by("-created")
    forums = sorted(forums, key=lambda x: x.num_posts() , reverse=True)
    forums = forums[0:conf_settings.POPULAR_FORUMS]
    return forums

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def top_3_tag(posts):
    all_tags = [tag for post in posts for tag in post.tags.all()]
    counter = Counter(all_tags)
    top_3 = counter.most_common(3)
    print(top_3)
    return [item[0] for item in top_3]