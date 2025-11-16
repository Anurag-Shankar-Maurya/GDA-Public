from django.test import TestCase


class UsersSmokeTest(TestCase):
    def test_index_or_login(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, (200, 302, 404))
from django.test import TestCase

# Create your tests here.
