from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.models import Subscription
class IndexPageView(TemplateView):
    template_name = 'main/index.html'



class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


def subscription_public_view(request):
    subscriptions = Subscription.objects.all()

    return render(request, 'subscription.html', {'subscriptions': subscriptions})

