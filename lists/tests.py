from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = u'족발과 새우젓'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = u'쌈도 샀니?'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)


        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        self.assertEqual(u'족발과 새우젓', first_saved_item.text)
        self.assertEqual(list_, first_saved_item.list)

        second_saved_item = saved_items[1]
        self.assertEqual(list_, second_saved_item.list)
        self.assertEqual(u'쌈도 샀니?', second_saved_item.text)


class NewListTest(TestCase):
    def test_save_post_request(self):
        self.client.post('/lists/new', data={'item_text':u'족발과 새우젓'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'족발과 새우젓')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text':u'족발과 새우젓'})
        self.assertRedirects(response, '/lists/the-unique-url/')


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_real_response(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertTrue(response.content.decode(), expected_html)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-unique-url/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Itemy 1', list=list_)
        Item.objects.create(text='Itemy 2', list=list_)

        response = self.client.get('/lists/the-unique-url/')
        self.assertContains(response, 'Itemy 1')
        self.assertContains(response, 'Itemy 2')
