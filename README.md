### Запуск
____
Для запуска необходимо всё скопировать в один проект, запустить сервер на одном терминале и клиент на другом

### Описание multiplication_server.py
____
- get_multiplier - возвращает объект из JSON, который потом обрабатывается отдельно
- get_number - получает число из объекта выше
- Класс MultiplicationServicer - методы для обработки запросов
  - __init__ - запуск для получения бд
  - GetMultiplier - получает объект из JSON
  - ListMultipliers - получаемый список цифр
  - RecordMultiplication - получаем сколько цифр, значение перемножения и тд.
  - serve - запуск сервера

### Описание multiplication_resources.py
____
read_multiplication_database - читаем JSON
### Описание multiplication_client.py
____
- format_point - возвращает str тех чисел что мы используем
- guide_list_multipliers - получаем список всех цифр которые есть
- generate_route - выбираем те цифры которые будут использоваться для рассчетов
- guide_record_multiplication - печатает статистическую инфу
- run - делает запрос на сервер и печатает основную инфу
