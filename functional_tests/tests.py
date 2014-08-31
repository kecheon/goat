__author__ = 'cheon'
#-*-coding:utf8-*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_input_exists(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 유저가 사이트 방문
        """

        :type self: object
        """
        self.browser.get(self.live_server_url)
        # title과 제목에 'TODO'가 있네...
        self.assertIn('TODO', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO', header_text)
        # todo list 항목 입력합니다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEquals(inputbox.get_attribute('placeholder'),
                          u'TODO 항목 입력')
        inputbox.send_keys('족발과 새우젓')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_input_exists(u'1: 족발과 새우젓')


        # 다른 TODO 입력을 할 수 있는 입력창이 열려있다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('쌈도 샀니?')
        inputbox.send_keys(Keys.ENTER)

        self.check_input_exists(u'1: 족발과 새우젓')
        self.check_input_exists(u'2: 쌈도 샀니?')

        # 다른 사람이 접속했다.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(u'족발과 새우젓', page_text)
        self.assertNotIn(u'쌈도 샀니?', page_text)

        # TODO 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(u'막걸리 추가')
        inputbox.send_keys(Keys.ENTER)
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(edith_list_url, francis_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(page_text, u'족발과 새우젓')
        self.assertIn(page_text, u'막걸리 추가')

        self.fail("End of tests!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')