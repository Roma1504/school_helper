import bs4
import re

class HasJsonElement:
    def get_json(self):
        new_data = {}
        for i, j in self.data.items():
            new_data[i] = get_json(j)
        
        return new_data

def get_json(element:HasJsonElement):
        
    
    if isinstance(element, HasJsonElement):
        return element.get_json()

    if isinstance(element, list):
        data = []
        for k in element:
            data.append(get_json(k))

        return data

    return element

class Lesson(HasJsonElement):
    def __init__(self, element):
        self.data = {}
        self.data['number'] = element.find(class_='dnevnik-lesson__number').text
        self.data['number'] = ''.join([i for i in self.data['number'] if i.isdigit()])
        if self.data['number'] != '':
            self.data['number'] = int(self.data['number'])
        self.data['time'] = element.find(class_='dnevnik-lesson__time').text
        self.data['subject'] = element.find(class_='js-rt_licey-dnevnik-subject').text
        self.data['home_task'] = element.find(class_='dnevnik-lesson__task')
        if self.data['home_task'] is not None:
            self.data['home_task'] = self.data['home_task'].text
            self.data['home_task'] = self.data['home_task'].replace('\n', '', self.data['home_task'].count('\n'))
        self.data['topic'] = element.find(class_='js-rt_licey-dnevnik-topic')
        if self.data['topic'] is not None:
            self.data['topic'] = self.data['topic'].text

class Day(HasJsonElement):
    def __init__(self, element):
        self.data = {}
        if element.find(class_='page-empty'):
            return
        self.data['title'] = element.find(class_='dnevnik-day__title').text
        self.data['lessons'] = []
        for i in element.find_all(class_='dnevnik-lesson'):
            self.data['lessons'].append(Lesson(i))