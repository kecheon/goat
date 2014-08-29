from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page

# Create your tests here.


# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)


class HomePageTesf(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


