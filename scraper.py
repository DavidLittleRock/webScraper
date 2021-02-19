
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
import re
import tkinter as tk


def get_my_urls():
    dg_latest = 'https://www.arkansasonline.com/news/latest/'
    dg_ar_news_1 = 'https://www.arkansasonline.com/news/news/arkansas/?page=1'
    dg_business = 'https://www.arkansasonline.com/news/business/'
    dg_world_news_1 = 'https://www.arkansasonline.com/news/news/nation-world/?page=1'
    dg_ar_politics = 'https://www.arkansasonline.com/news/news/politics/arkansas/'
    my_urls = [dg_latest, dg_ar_news_1, dg_business, dg_world_news_1, dg_ar_politics]
    return my_urls


def make_file():
    headers = ['title', 'lead', 'byline', 'link']
    with open('news_file.csv', 'w') as file_write:
        writer_obj = csv.writer(file_write)
        writer_obj.writerow(headers)


def build_file():
    make_file()
    for url in get_my_urls():
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        with urlopen(req) as uclient:
            print(uclient.status)
            page_html = uclient.read()
        page_soup = soup(page_html, 'html.parser')
        containers = page_soup.findAll('div', {'class': 'recommended-article'})
        with open('news_file.csv', 'a') as file_write:
            writer_obj = csv.writer(file_write)
            for container in containers:
                title = container.find('span', {'class': 'recommended__article-title'}).text.strip()
                lead = container.find('span', {'class': 'recommended__article-lead'}).text.strip()
                byline = container.find('span', {'class': 'recommended__article-bi-line'}).text
                link = 'https://arkansasonline.com'+container.find('a').get('href')
                writer_obj.writerow([title, lead, byline, link])
                # print(link)
    #  use pandas dataframe to remove duplicates
    df = pd.read_csv('news_file.csv')
    # print(df)
    ndf = df.drop_duplicates().reset_index(drop=True)
    # print(ndf)
    ndf.to_csv('news_file_out.csv', index=False)


def reformat_news():
    # df = pd.read_csv('news_file_out.csv')
    # print(df.head())
    # print(df.title)
    # for row in df:
        # print(row)
        # print(df[row])

    with open('news_file_out.csv', 'r') as read_file:
        reader_obj = csv.reader(read_file)
        with open('news_email.txt', 'w') as write_file:
            # write_file.write("new email")
            # writer_obj = csv.writer(write_file)
            write_file.write("new email")
            for line in reader_obj:
                print(f"Title: {line[0]} \n\tLead: {line[1]} \n\tLink: {line[3]} \n")
                # writer_obj.writerow(f"Title: {line[0]} \n\tLead: {line[1]} \n\tLink: {line[3]} \n")
                write_file.write(f"Title: {line[0]} \n\tLead: {line[1]} \n\tLink: {line[3]} \n")

    with open('news_email.txt', 'r') as read_file:
        print('email file ------------------------')
        # print(read_file.read())
        tk_file = read_file.read()
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print(tk_file)
    return tk_file

if __name__ == '__main__':
    # main()
    build_file()
    # reformat_news()

    window = tk.Tk()
    window.title('title of window')
    window.geometry('600x400')
    listss = reformat_news()
    new_label = tk.Label(text=listss)
    new_label.grid(column=0, row=0)
    window.mainloop()

    # build_file()
    # reformat_news()