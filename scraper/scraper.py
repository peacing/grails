from selenium import webdriver
import re
import time
import datetime


class GrailScraper:

    def __init__(self, designer):
        self.designer = designer
        self.base_url = 'https://www.grailed.com/designers/'
        #self.driver = webdriver.PhantomJS(executable_path=
        #              '/Users/paulsingman/.node_modules_global/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
        self.driver = webdriver.Chrome()
        self.item_links_and_data = []
        self.total_items = 0
        self.items_per_page = 40
        self.page = 1

    def get_designer_homepage(self):
        self.driver.get(self.base_url + self.designer)
        time.sleep(1)
        return

    def build_paginated_url(self):

        paginated_url =  self.base_url + self.designer + '?page=' + str(self.page)
        self.page += 1
        print('working on page {}'.format(self.page))
        return paginated_url

    def get_paginated_url(self, new_url):
        self.driver.get(new_url)
        time.sleep(1)
        return

    def get_item_count(self):

        for elem in self.driver.find_elements_by_class_name('individual-designer-stat-container'):
            amount = elem.find_element_by_tag_name('div').text
            self.total_items += int(amount)

        print('total items: {}'.format(self.total_items))
        return

    def get_item_links_and_info(self):

        for item in self.driver.find_elements_by_css_selector('div.feed-item'):

            """
            date_ago = item.find_element_by_class_name('date-ago').text
            try:
                bumped_date = item.find_element_by_css_selector('span.bumped.date-ago').text
            except:
                bumped_date = None
            brand = item.find_element_by_css_selector('h3.listing-designer.truncate').text
            size = item.find_element_by_css_selector('h3.listing-size.sub-title.bold').text
            product = item.find_element_by_css_selector('h3.sub-title.listing-title').text
            try:
                curr_price = item.find_element_by_css_selector('h3.sub-title.bold.new-price').text
                original_price = item.find_element_by_css_selector(
                    'h3.sub-title.bold.original-price.strike-through').text
            except:
                original_price = None
                curr_price = item.find_element_by_css_selector('h3.sub-title.bold.original-price').text

            """
            # link = item.find_element_by_xpath("//a[contains(@href,'/listings/')]").get_attribute('href')
            link = item.find_element_by_css_selector('a').get_attribute('href')
            match = re.search('listings/(\d{5,7})-', link)
            prod_id = match.group(1)

            self.total_items -= 1
            #self.item_links_and_data.append([prod_id, brand, product, size, date_ago, curr_price,
            #                                 bumped_date, original_price, link])
            self.item_links_and_data.append([prod_id, link])

    def get_all_links(self):

        self.get_designer_homepage()

        self.get_item_count()

        self.get_item_links_and_info()

        while self.total_items > 40:

            next_page_url = self.build_paginated_url()

            self.get_paginated_url(next_page_url)
            self.get_item_links_and_info()

        next_page_url = self.build_paginated_url()
        self.get_paginated_url(next_page_url)
        self.get_item_links_and_info()

        print('Items remaining: {}'.format(self.total_items))

        self.driver.close()

        return self.item_links_and_data


if __name__ == '__main__':

    g = GrailScraper('common-projects')
    cp_data = g.get_all_links()

    print(len(cp_data))
    print(cp_data)

