FROM python:3.10.7
RUN mkdir -p /telegram_bot/common_modules && mkdir /telegram_bot/sys
WORKDIR /telegram_bot
ADD ["./telegram_bot", "/telegram_bot"]
ADD ["./common_modules", "/telegram_bot/common_modules"]
ADD ["./sys", "/telegram_bot/sys"]
COPY [".env", "settings.yaml", "."]
RUN pip3 install -r /telegram_bot/requirements.txt
CMD [ "python", "/telegram_bot/run_bot.py" ]