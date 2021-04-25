
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from time import sleep
 
class Trans(object):
    def __init__(self,timeout= None):
        self.timout = timeout
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
 
        #有界面模式
        # self.browser = webdriver.Chrome()
 
    def __del__(self):
        self.browser.close()
 
    def get_trans(self):
        self.browser.get("https://translate.google.cn/")
        words = self.input_words()
        self.browser.find_element_by_id("source").send_keys(words)
        sleep(1)
        self.working(words)
 
    def working(self,words):
        page_html = self.browser.page_source
        page_tree = etree.HTML(page_html)
        res_items = []
        res_item = {}
        my_result = page_tree.xpath("//div[@class='source-target-row']//span/span[1]/text()")[0].strip()
        res_item['{}'.format(words)] = my_result
        res_items.append(res_item)
        # print(res_items)
        print("{} 翻译结果是:{}".format(words, my_result))
 
        #写入文件:
        save_it = input("回车保存至本地,任意字符不保存:")
        if save_it =="":
            res_ = "{}-----------{}".format(my_result, words)
            with open(r".\word_book.txt", 'a', encoding='utf8') as fp:
                fp.write(res_)
                fp.write("\n")
                fp.close()
        else:
            pass
        
 
    def input_words(self):
        words = input("请输入要翻译的文字:")
        language = input("要翻译成的语言(中文/英文):")
        if language == "英文":
            self.browser.find_element_by_xpath("//div[@class='tl-sugg']//div[@id='sugg-item-en']").click()
            sleep(1)
        elif language == "中文":
            self.browser.find_element_by_xpath("//div[@class='tl-sugg']//div[@id='sugg-item-zh-CN']").click()
            sleep(1)
        # 默认翻译成英文
        else:
            self.browser.find_element_by_xpath("//div[@class='tl-sugg']//div[@id='sugg-item-en']").click()
            sleep(1)
            # pass
        # words = "人工智能"
        return words
 
if __name__ == '__main__':
    process = Trans()
    process.get_trans()
