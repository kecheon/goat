from django.test import TestCase
from lists.models import Item, List


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