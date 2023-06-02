from django import forms
from django_forum_app.models import Topic, Post, Comment, ProfaneWord
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _
from django.conf import settings

TINYMCE_DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {
    "language": 'en',
    "theme": "modern",
    "height": 600,
    "plugins": [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste",
    ],
    "toolbar": "styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview",
    "menubar": False,
    "media_alt_source": False,
    "media_poster": False,
    "media_dimensions": False,
})

DJANGO_FORUM_APP_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_FORUM_APP_FILTER_PROFANE_WORDS', False)


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(
        attrs={'class':'mce-here','cols': 80, 'rows': 30, 'placeholder': _("Your answer...")}, mce_attrs=TINYMCE_DEFAULT_CONFIG))

    tags = forms.CharField(
        label='Tags',
        help_text=_('Add upto 5 comma separated tags'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. (tag1, tag2, tag3)')})
    )

    class Meta:
        model = Post
        fields = ('body',)


class TopicForm(forms.ModelForm):

    title = forms.CharField(label=_("Title"), max_length=60, required=True)
    description = forms.CharField(label=_("First message"), widget=TinyMCE(
        attrs={'class':'mce-here', 'cols': 80, 'rows': 30, 'placeholder': _("Write your answer here!")}, mce_attrs=TINYMCE_DEFAULT_CONFIG))

    class Meta():
        model = Topic
        fields = ('title', 'description')


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Title')})
    )
    body = forms.CharField(label=_('Body'), widget=TinyMCE(
        attrs={'class':'mce-here', 'cols': 40, 'rows': 30, 'placeholder': _("Your answer...")}, mce_attrs=TINYMCE_DEFAULT_CONFIG))

    tags = forms.CharField(
        label='Tags',
        help_text=_('Add upto 5 comma separated tags'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. (tag1, tag2, tag3)')})
    )

    class Meta():
        model = Post
        exclude = ('creator', 'updated', 'created', 'topic', 'user_ip', 'telegram_id')

    '''def __init__(self, *args, **kwargs):
        enable_my_bool = kwargs.pop('enable_my_bool', False) # False is the default
        super(PostForm, self).__init__(*args, **kwargs)
        if enable_my_bool:
            self.fields = ('body', 'title')
        else:
            self.fields = ()'''

    def clean_body(self):
        body = self.cleaned_data["body"]

        if DJANGO_FORUM_APP_FILTER_PROFANE_WORDS:
            profane_words = ProfaneWord.objects.all()
            bad_words = [w for w in profane_words if w.word in body.lower()]

            if bad_words:
                raise forms.ValidationError(_("Bad words like '%s' are not allowed in posts.") % (reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))

        return body

class CommentForm(forms.ModelForm):
    text = forms.CharField(label=False, widget=TinyMCE(
        attrs={'class':'mce-here', 'cols': 40, 'rows': 20, 'placeholder': _("Your answer...")}, mce_attrs=TINYMCE_DEFAULT_CONFIG))

    class Meta():
        model = Comment
        exclude = ('creator', 'updated', 'created', 'post',)

    def clean_body(self):
        body = self.cleaned_data["body"]

        if DJANGO_FORUM_APP_FILTER_PROFANE_WORDS:
            profane_words = ProfaneWord.objects.all()
            bad_words = [w for w in profane_words if w.word in body.lower()]

            if bad_words:
                raise forms.ValidationError(_("Bad words like '%s' are not allowed in posts.") % (reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))

        return body