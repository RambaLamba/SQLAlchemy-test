# SQLAlchemy/База данных книжного магазина


*Модели классов SQLAlchemy содержатся в файле "models.py"*
-

В файле "main.py" содержатся:

*Скрипт для выборки магазинов, продающих целевого издателя:*
-
- подключается к БД PostgreSQL;
- импортирует необходимые модели данных;
- принимает имя или идентификатор издателя (publisher). Выводит построчно факты покупки книг этого издателя.

*Скрипт для заполнения БД тестовыми данными*
- 
В файле "test_data.json" находятся тестовые данные.

Рекомендации по использованию:

1) Сначала заполните базу данных, вызвав fill_data(session);

2) Затем выполните запрос с помощью get_sales_by_publisher()
