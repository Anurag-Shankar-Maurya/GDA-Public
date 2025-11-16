from django.test import TestCase


class ContentManagementSmokeTest(TestCase):
    def test_homepage_or_index(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, (200, 302, 404))
from django.test import TestCase

# Create your tests here.
