# turnip_exchange_monitoring

Telegram бот для мониторинга предложений о продаже репы на turnip.exchange

<a align="center" href="https://github.com/Andrey-Guryanov/turnip_exchange_monitoring/raw/main/scheme.jpg"><img src="https://github.com/Andrey-Guryanov/turnip_exchange_monitoring/raw/main/scheme.jpg" width="350" tex/></a>

Доступные функционалы:

- :white_check_mark: выбор языка (rus / eng)
- :white_check_mark: просмотр доступных для продажи островов
- :white_check_mark: оповещения о появлении нового острова с ценой выше заданной и очередью менее 5 пользователей.

____

## Быстрый старт

1. В директорию `./firefox_driver` поместите актуальную версию geckodriver для linux 64 (
   см. https://github.com/mozilla/geckodriver/releases/). Должно получиться так: `./firefox_driver/geckodriver_linux_64`
   ;
2. Измените пароль для MongoDB в файле `docker-compose.yml`: MONGO_INITDB_ROOT_PASSWORD={новый пароль} ;
3. В директории с проектом создайте файл `.env` (см. пример - файл `.env_example`) со следующим содержанием:
    ```
    TELEGRAM_TOKEN={telegram_token}
    
    MONGO_USER=root
    MONGO_PASS={пароль для MongoDB из п. 2}
    MONGO_HOST=container_mongo
    ```
4. В директории с проектом выполнить "docker-compose up"
