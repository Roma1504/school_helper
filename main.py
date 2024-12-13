import http.client
import json
import eel
import bs4
from day import Day

eel.init('web')

# Глобальная переменная для хранения куки
cookies = ''

# Чтение данных для входа из файла
def read_login_data():
    with open('data.json', 'r', encoding='ascii') as file:
        return json.load(file)

# Запись данных в JSON-файл с кодировкой ASCII
def write_json_ascii(data):
    with open('data.json', 'w', encoding='ascii') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)

# Метод для отправки запросов и сохранения куки
def send_request(method, url, headers={}, body=None):
    global cookies
    
    if cookies:
        headers['Cookie'] = cookies
    
    conn = http.client.HTTPSConnection('edu.rk.gov.ru')
    conn.request(method, url, body=body, headers=headers)
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    response_cookies = response.getheader('Set-Cookie')
    conn.close()
    
    if response_cookies:
        cookies += '; ' + response_cookies if cookies else response_cookies
    
    return content

@eel.expose
def authorize(username, password):
    global cookies
    data = {'username': username, 'password': password}
    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    
    content = send_request('POST', '/ajaxauthorize', headers=headers, body=payload)
    response_data = json.loads(content)

    if not response_data['result']:
        return response_data
    
    redirect_url = response_data['actions'][0]['url']
    content = send_request('GET', redirect_url)

    return response_data

@eel.expose
def get_journal_data():
    content = send_request('GET', 'https://edu.rk.gov.ru/journal-app/')
    soup = bs4.BeautifulSoup(content, 'html.parser')
    days:bs4.element.Tag = soup.find_all(class_='dnevnik-day')
    data = []
    for day in days:
        data.append(Day(day).get_json())
    return data

@eel.expose
def get_tasks(date):
    if not read_login_data().get('task', False):
        data = get_journal_data()
        for i in data:
            if i == {}:
                continue
            if date in i['title']:
                day = i['lessons']
                break
        json_data = read_login_data()
        json_data['task'] = {'date':date, 'tasks':day}
        write_json_ascii(json_data)
    return read_login_data()['task']

if read_login_data().get('username', False):
    authorize(read_login_data()['username'], read_login_data()['password'])
    eel.start('welcome.html')
else:
    eel.start('login.html')
