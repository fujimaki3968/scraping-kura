import requests
from bs4 import BeautifulSoup

def scrapingKura():
    url_path = "https://www.kurasushi.co.jp/menu/?area=area0"
    request = requests.get(url_path)
    soup = BeautifulSoup(request.content, "html.parser")
    menu = soup.find('div', class_='menu-wrap').find_all('div', class_='section-body')

    data = {'menu': []}

    for index, category in enumerate(menu):
        category_name = category.find('h3', class_='menu-section-heading').text
        menu_list = category.find_all('div', class_='menu-item')
        list = []
        for item in menu_list:
            area = item['class']
            area.remove('menu-item')
            name = item.find('h4', class_='menu-name').text.replace('\u3000', ' ')
            summary = item.find_all('li')
            price = summary[0].find_all('p')[0].text.replace('円（税抜）', '')
            calorie = summary[0].find_all('p')[1].text.replace('kcal', '')

            try:
                if summary[-1].find_all('p')[1].text == '可':
                    delivery = True
                else:
                    delivery = False
            except:
                delivery = False
                print(summary)

            payload = {
                'name': name,
                'price': int(price),
                'calorie': int(calorie),
                'areas': area,
                'delivery': delivery
            }

            list.append(payload)
        data['menu'].append({
            'category_name': category_name,
            'menu_data': list
        })
    return data

if __name__ == '__main__':
    data = scrapingKura()
    print(data)