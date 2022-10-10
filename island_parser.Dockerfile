FROM python:3.10.7
RUN mkdir -p island_parser/common_modules && mkdir island_parser/firefox_driver
WORKDIR /island_parser
ADD ["./island_parser", "/island_parser"]
ADD ["./common_modules", "/island_parser/common_modules"]
ADD ["./firefox_driver", "/island_parser/firefox_driver"]
COPY [".env", "settings.yaml", "."]
RUN pip3 install -r /island_parser/requirements.txt && apt-get update && apt-get install -y --no-install-recommends firefox-esr
CMD [ "python", "/island_parser/run_parser.py" ]