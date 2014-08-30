__author__ = 'cheon'
#-*-coding:utf8-*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 유저가 사이트 방문
        self.browser.get("http://localhost:8000")
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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == u'1: 족발과 새우젓' for row in rows),
            "입력한 내용이 테이블에 없습니다."
        )

        self.assertEquals()
        self.fail("End of tests!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')