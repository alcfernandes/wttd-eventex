import unittest

from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """Get/ Most return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Most subscriptions/subscription_form.html as template"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""

        tags = ( ('<form', 1),
                 ('<input', 6),
                 ('type="text"', 3),
                 ('type="email"', 1),
                 ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        # {'nome': 'alessandro', 'cidade': 'Valença', 'estado': 'RJ'}
        data = {'name': 'Alessandro Fernandes', 'cpf': '00746198701', 'email': 'alcfernandes@yahoo.com',
                'phone': '24998829105'}

        #data = dict(name="Alessandro Fernandes", cpf="00746198701", email="alcfernandes@yahoo.com",
        #            phone="24998829105")
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Valid post shoud redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscrib_email(self):
        """Most send one email"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Invalid POST shoud not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Henrique Bastos', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')




# Versao antes de implementar o /inscricao/1/
#class SubscribeSuccessMessage(TestCase):
#    def test_message(self):
#        data = dict(name='Alessandro Fernandes', cpf='00746198701',
#                    email='alcfernandes@yahoo.com', phone='24998829105')
#
#        response = self.client.post('/inscricao/', data, follow=True)
#
#        self.assertContains(response, 'Inscrição realizada com sucesso!')