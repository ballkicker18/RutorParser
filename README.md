# Rutor Parser

Простой скрипт для просмотра торрентов на руторе.
![Screen](screens/screenshot.png)
![Second Screen](screens/screenshot_2.png)
![Third Screen](screens/screenshot_3.png)

Есть возможность поиска и открытия торрентов в браузере.

## Установка

Клонируйте репозиторий:
```bash
git clone https://github.com/ballkicker228/RutorParser
```
Перейдите в папку:
```bash
cd RutorParser
```
Установите зависимости:
```bash
./install.sh
```
Теперь можно запускать скрипт:
```bash
./start.sh
```

## TODO

- ~~Добавить gui~~
- Сделать поиск по категориям
- Искать по всем страницам результатов
- Добавить диалоговое окно для просмотра описания торрента
- Сделать авторизацию по cookie и скачивание торрентов из скрипта
- Производить запросы в отдельных потоках чтобы не блокировался интерфейс
