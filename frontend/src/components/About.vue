<template>
    <div class="features">
        <h1>Выберите тест</h1>
        {% if quizes %}
            {% for el in quizes %}

                <div class ="alert alert-warning">
                    <h3>{{ el.name }}</h3>
                    <p>Количество вопросов: {{ el.number_of_questions }}</p>
                    <a href="{% url 'quiz-view' el.id %}" class="btn btn-warning">Пройти тестирование</a>
                </div>
            {% endfor %}
        {% else %}}
            <p>Тесты украли инопланетяне</p>
        {% endif %}
    </div>
</template>
