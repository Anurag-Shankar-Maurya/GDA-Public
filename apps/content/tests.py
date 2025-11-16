from django.test import TestCase

# Create your tests here.


class SmokeTest(TestCase):
	def test_homepage_loads(self):
		# A simple smoke test that asserts the site returns a response for root URL
		response = self.client.get('/')
		# Allow either 200 (if root view exists) or 404 if no route defined yet
		self.assertIn(response.status_code, (200, 302, 404))
