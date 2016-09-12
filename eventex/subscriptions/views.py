from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:  # É GET
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    _send_mail(context=form.cleaned_data,
               from_=settings.DEFAULT_FROM_EMAIL,
               subject='Confirmação de inscricao',
               template_name='subscriptions/subscription_mail.txt',
               to=form.cleaned_data['email'])

    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def _send_mail(context, from_, subject, template_name, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject,
                   body,
                   from_,
                   [from_, to])