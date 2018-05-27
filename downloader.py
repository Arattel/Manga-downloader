from bs4 import  *
import requests
import os


def download_image_by_link(image_link, path):
    """
    (str, str) -> None
    Downloads an image by link
    """
    url = image_link
    r = requests.get(url, allow_redirects=True)
    open(path, 'wb').write(r.content)



def chapters(link):
    """
    (str) -> (dict)
    Finds name and  chapter links by link of main page
    """
    site = requests.get(link)
    site = site.text
    site = BeautifulSoup(site, 'html.parser')
    name = site.find_all('h1')[0].getText()
    site = site.find_all('div', class_ = 'chapter-list')[0]
    site = site.find_all('div', class_ = 'row')
    for i in range(len(site)):
        site[i] = site[i].find_all('a')[0]['href']
    site.reverse()
    os.makedirs(name, exist_ok=True)
    return {'name': name, 'chapters': site}


def download_all_pages(html, directory):
    """
    (str, str) -> None
    downloads all pages by link and directory name
    """
    html = requests.get(html).text
    site = BeautifulSoup(html, 'html.parser')
    name = site.find_all('div', class_ = 'info-top-chapter')
    name = name[0]
    name = name.find_all('h2')[0].get_text()
    print(name)
    folder = directory + '/' + name
    os.makedirs(folder, exist_ok=True)
    pages = site.find_all('div', class_ = 'vung-doc')
    pages = pages[0]
    pages = pages.find_all('img')
    for i in pages:
        print(i['title'], i['src'])
        download_image_by_link(i['src'], folder + '/' + i['title'] + '.jpg')


def main(link):
    """
    (str) -> None
    Downloads the whole manga by given link into directory with name
    """
    data = chapters(link)
    chapters_list = data['chapters']
    name = data['name']
    for i in chapters_list:
        download_all_pages(i, name)


if __name__ == '__main__':
    # download_image_by_link("http://s1.mgimgcdn.com/b2/buccafe/chapter_15/2.jpg", '1.jpg')
    main("http://mangakakalot.com/manga/journey_to_the_west")