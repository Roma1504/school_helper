import bs4
import re

class HasJsonElement:
    def get_json(self):
        new_data = {}
        for i, j in self.data.items():
            new_data[i] = get_json(j)
        
        return new_data

def get_json(element: HasJsonElement):
    if isinstance(element, HasJsonElement):
        return element.get_json()

    if isinstance(element, list):
        data = []
        for k in element:
            data.append(get_json(k))

        return data

    return element

def get_lesson(element):
    lesson_data = {}
    lesson_data['number'] = element.find(class_='dnevnik-lesson__number').text
    lesson_data['number'] = ''.join([i for i in lesson_data['number'] if i.isdigit()])
    if lesson_data['number'] != '':
        lesson_data['number'] = int(lesson_data['number'])
    lesson_data['time'] = element.find(class_='dnevnik-lesson__time').text
    lesson_data['subject'] = element.find(class_='js-rt_licey-dnevnik-subject').text
    lesson_data['home_task'] = element.find(class_='dnevnik-lesson__task')
    if lesson_data['home_task'] is not None:
        lesson_data['home_task'] = lesson_data['home_task'].text
        lesson_data['home_task'] = lesson_data['home_task'].replace('\n', '', lesson_data['home_task'].count('\n'))
    lesson_data['topic'] = element.find(class_='js-rt_licey-dnevnik-topic')
    if lesson_data['topic'] is not None:
        lesson_data['topic'] = lesson_data['topic'].text
    
    return lesson_data

def get_day(element):
    day_data = {}
    if element.find(class_='page-empty'):
        return None
    day_data['title'] = element.find(class_='dnevnik-day__title').text
    day_data['lessons'] = []
    for i in element.find_all(class_='dnevnik-lesson'):
        day_data['lessons'].append(get_lesson(i))
    
    return day_data