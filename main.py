import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_c(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    catalog = soup.find('div', class_="search-results-table")
    cars = catalog.find_all('div', class_="list-item list-label")
    
    for car in cars:
        title = car.find('h2', class_='name').text.strip()
        price = car.find('div', class_="block price").find('strong').text
        image = car.find('img', class_="lazy-image").get('data-src')
        content = car.find('div', class_="block info-wrapper item-info-wrapper").text.strip().split('\n')
        cont = ','.join([(i.strip()) for i in content])
        
        write_csv({'title':title, 'price':price, 'image':image, 'content':cont})
        

        
def write_csv(data):
    with open('cars.csv', 'a') as file:
        name = ['title', 'price', 'content', 'image']
        write = csv.DictWriter(file, delimiter=',', fieldnames=name)
        write.writerow(data)




def main():
    for i in range(100):
        url = f'https://www.mashina.kg/search/all/?page={i}'
        html = get_html(url)
        soup = get_c(html)
        get_data(soup)


if __name__ == '__main__':
    main()