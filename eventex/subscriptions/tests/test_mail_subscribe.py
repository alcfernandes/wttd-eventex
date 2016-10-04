import unittest

from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):

        data = dict(name="Alessandro Fernandes", cpf="00746198701", email="alcfernandes@yahoo.com",
                    phone="24998829105")
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_mail_subject(self):
        expected = "Confirmação de inscricao"

        self.assertEqual(expected, self.email.subject)

    def test_subscription_mail_from(self):
        expected = "contato@eventex.com.br"

        self.assertEqual(expected, self.email.from_email)

    def test_subscription_mail_to(self):
        expected = ['contato@eventex.com.br', 'alcfernandes@yahoo.com']

        self.assertEqual(expected, self.email.to)

    def test_subscription_mail_body(self):

        contents = [
            'Alessandro Fernandes',
            '00746198701',
            'alcfernandes@yahoo.com',
            '24998829105',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

