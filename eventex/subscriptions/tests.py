from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get/ Most return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Most subscriptions/subscription_form.html as template"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must contain 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name="Alessandro Fernandes", cpf="00746198701", email="alcfernandes@yahoo.com",
                    phone="24998829105")
        self.resp = self.client.post("/inscricao/", data)

    def test_post(self):
        """Valid post shoud redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscrib_email(self):
        """Most send one email"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_mail_subject(self):
        email = mail.outbox[0]
        expected = "Confirmação de inscricao"

        self.assertEqual(expected, email.subject)

    def test_subscription_mail_from(self):
        email = mail.outbox[0]
        expected = "contato@eventex.com.br"

        self.assertEqual(expected, email.from_email)

    def test_subscription_mail_to(self):
        email = mail.outbox[0]
        expected = ['contato@eventex.com.br', 'alcfernandes@yahoo.com']

        self.assertEqual(expected, email.to)

    def test_subscription_mail_body(self):
        email = mail.outbox[0]
        self.assertIn('Alessandro Fernandes', email.body)
        self.assertIn('00746198701', email.body)
        self.assertIn('24998829105', email.body)
        self.assertIn('alcfernandes@yahoo.com', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

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


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Alessandro Fernandes', cpf='00746198701',
                    email='alcfernandes@yahoo.com', phone='24998829105')

        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso!')