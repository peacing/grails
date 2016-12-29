import requests
from selenium import webdriver


class Scraper:

    def __init__(self):
        self.base_url = 'https://www.grailed.com/designers/common-projects'
        self.driver = webdriver.Chrome()
        self.item_links = []
        self.total_items = 0

    def get_designer_homepage(self):
        self.driver.get(self.base_url)

    def get_item_count(self):

        for elem in self.driver.find_elements_by_class_name('individual-designer-stat-container'):
            amount = elem.find_element_by_tag_name('div').text
            self.total_items += int(amount)

    def get_item_links(self):

        for item in self.driver.find_elements_by_css_selector('div.feed-item'):
            link = item.find_element_by_xpath("//a[contains(@href,'/listings/')]").get_attribute('href')
            self.item_links.append(link)









if __name__ == '__main__':

    pass