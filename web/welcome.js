function createElement(text, className, elementName, parent) {
    const element = document.createElement(elementName);
    element.className = className;
    element.textContent = text; // Используем textContent вместо innerHTML для безопасности
    parent.appendChild(element);
    return element;
}

eel.get_journal_data()(function(response) {
    const daysContainer = document.getElementById("days");
    const fragment = document.createDocumentFragment(); // Создаем фрагмент для оптимизации

    response.forEach(day => {
        if (!day.title || !day.lessons) return; // Проверка на falsy значение

        const dayElement = createElement('', "day", "div", fragment);
        createElement(day.title, "day_title", "p", dayElement);
        
        const lessonsElement = createElement('', "lessons", "div", dayElement);
        
        day.lessons.forEach(lesson => {
            const lessonElement = createElement('', "lesson", "div", lessonsElement);
            createElement(lesson.number, "lesson_number", "p", lessonElement);
            createElement(lesson.subject, "lesson_subject", "p", lessonElement);
            createElement(lesson.time, "lesson_time", "p", lessonElement);

            if (lesson.home_task) {
                createElement(lesson.home_task, 'lesson_home_task', 'p', lessonElement);
            }
            if (lesson.topic) {
                createElement(lesson.topic, 'lesson_topic', 'p', lessonElement);
            }
        });
    });

    daysContainer.appendChild(fragment); // Добавляем все элементы за один раз
});