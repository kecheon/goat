__author__ = 'cheon'
#-*-coding:utf8-*-
from .base import FunctionalTest
# from pyvirtualdisplay import Display
#
# display = Display(visible=0, size=(1024, 768))
# display.start()


class StyleAndLayoutTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']
                               + inputbox.size['width']/2,
                               512,
                               delta=5
        )
        inputbox.send_keys(u'껍데기도\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']
                               + inputbox.size['width']/2,
                               512,
                               delta=5
        )

