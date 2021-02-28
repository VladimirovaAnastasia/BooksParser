# Парсер книг с сайта tululu.org

Скрипт предоставляет информацию о книгах с сайта [tululu.org](tululu.org), а также сохраняет их содержимое для того, чтобы в дальнейшем книгами можно было наслаждаться без наличия интернета.
![взломщик Вова](https://dvmn.org/media/lessons/books_1_F7MUA7w.jpg)

При запуске скрипта в консоль для каждой книги выводится ее заголовок, автор, жанр, комментарии пользователей.
Также в папку books скачивается ее содержимое в формате txt. В папку images сохраняются обложки книг. Если указанное id книги не найдено, скрипт вас об этом уповестит. Диапазон id книг, в свою очередь, необходимо указать при запуске скрипта.

[Пример странички с книгой](https://tululu.org/b9/).

## Как запустить
 Устанавливаем необходимые библиотеки
 ```
 pip install requirements.txt
```
 Запускаем скрипт командой 
 ```
 python script.py --start_id start_id --end_id end_id
 ```
 `start_id` - id книги, с которой начать парсинг (по умолчанию - 1),

`end_id` - id книги, на которой закончить парсинг (по умолчанию - 10).
 
 
 Например: 
 
  ```
 python script.py --start_id 5 --end_id 18
 ```
 
## Цель проекта
 Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/) 
