import time
import datetime
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

def connent_url(UrlPath):
    time.sleep(3)
    Data_List = []
    df = pd.read_csv(UrlPath)

    i = 1
    for url in df:
        driver.get(url=url)
        try:
            page = 0
            for y in range(100):
                js = 'window.scrollBy(0,1000)'
                driver.execute_script(js)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                divs = soup.find_all(
                    'div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
                print(divs)
                page += 1
                print('正在下列页面获取数据 {}'.format(page))

                for div in divs:
                    data_list = []
                    name = div.find(
                        'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
                    data_list.append(name)
                    user_name = div.find(
                        'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t'}).get_text()
                    data_list.append(user_name)
                    date = div.find('time')
                    data_list.append(date['datetime'])
                    content = div.find('div', {
                        'class': 'css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}).get_text()
                    data_list.append(str(content).strip().replace('\n', ''))
                    Data_List.append(data_list)
                time.sleep(3)
        except Exception as e:
            print(e)
        print('第 {} 个URL信息已获取完毕'.format(i))
        i = i + 1

    driver.close()

    Data_List_New = []
    for data in Data_List:
        if data not in Data_List_New:
            Data_List_New.append(data)
    return Data_List_New

def Save_Data(UrlPath):
    Data_List_New = connent_url(UrlPath=UrlPath)
    print('共爬取了 {} 条数据'.format(len(Data_List_New)))
    df_Sheet = pd.DataFrame(Data_List_New, columns=[
                            'name', 'user_name', 'date', 'content'])
    print('Get data successfully!')

    TIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.now().strftime(TIMEFORMAT)
    
    # csv_path = 'twitter_crawler/twitter_data/crawl_log(' + now + ').csv'
    # df_Sheet.to_csv(csv_path)
    
    excel_path = 'twitter_crawler/twitter_data/crawl_log(' + now + ').xlsx'
    writer = pd.ExcelWriter(excel_path)
    df_Sheet.to_excel(excel_writer=writer, sheet_name='twitter', index=None)
    writer.save()
    print('Save successfully!')
    writer.close()
    print('Close successfully!')

def Run():
    Save_Data(UrlPath='twitter_crawler/twitter_url.txt')

if __name__ == '__main__':
    Run()