from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name="Alessandro Fernandes",
            cpf="00746198701",
            email="alcfernandes@yahoo.com",
            phone="24-998829105"
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr. """
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Alessandro Fernandes', str(self.obj))

    def test_paid_default_to_false(self):
        """By default paid must be False."""

        self.assertEqual(False, self.obj.paid)