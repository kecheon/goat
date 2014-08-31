from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string

# Create your tests here.


# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_real_response(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertTrue(response.content.decode(), expected_html)

    def test_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = u'족발과 새우젓'
        response = home_page(request)

        self.assertIn(u'족발과 새우젓', response.content.decode())

