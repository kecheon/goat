from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List


class NewListTest(TestCase):
    def test_save_post_request(self):
        self.client.post('/lists/new', data={'item_text':u'족발과 새우젓'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'족발과 새우젓')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text':u'족발과 새우젓'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id))


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
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Itemy 1', list=correct_list)
        Item.objects.create(text='Itemy 2', list=correct_list)

        another_list = List.objects.create()
        Item.objects.create(text='another Itemy 1', list=another_list)
        Item.objects.create(text='another Itemy 2', list=another_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Itemy 1')
        self.assertContains(response, 'Itemy 2')
        self.assertNotContains(response, 'another Itemy 1')
        self.assertNotContains(response, 'another Itemy 2')


class NewItemTest(TestCase):

    def test_can_save_post_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()

        self.client.post('/lists/%d/add_item' % (correct_list.id),
                         data={'item_text':u'족발과 새우젓'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'족발과 새우젓')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' % (correct_list.id),
                                    data={'item_text':u'족발과 새우젓'})

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id))

    def test_passes_correct_list_to_template(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (correct_list.id))
        self.assertEqual(response.context['list'], correct_list)