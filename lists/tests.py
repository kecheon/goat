from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.

class ItemTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = u'족발과 새우젓'
        first_item.save()

        second_item = Item()
        second_item.text = u'쌈도 샀니?'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        self.assertEqual(u'족발과 새우젓', first_saved_item.text)

        second_saved_item = saved_items[1]
        self.assertEqual(u'쌈도 샀니?', second_saved_item.text)

    def test_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = u'족발과 새우젓'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'족발과 새우젓')
        # self.assertIn(u'족발과 새우젓', response.content.decode())
        # expected_html = render_to_string('home.html',
        #                                  {'new_item_text':u'족발과 새우젓'})
        # self.assertEqual(response.content.decode(), expected_html)

    def test_post_redirect(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = u'족발과 새우젓'
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_save_only_not_none(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)



class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_real_response(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertTrue(response.content.decode(), expected_html)

    def test_display_all_items(self):
        Item.objects.create(text='Itemy 1')
        Item.objects.create(text='Itemy 2')
        request = HttpRequest()
        response = home_page(request)

        self.assertIn('Itemy 1', response.content.decode())
        self.assertIn('Itemy 2', response.content.decode())