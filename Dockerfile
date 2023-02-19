FROM python:3.7.16

COPY ./project/resources/paquetes_necesarios.txt .

RUN pip install -r paquetes_necesarios.txt

COPY ./project ./project
WORKDIR ./project

ENV TERM xterm

CMD ["python", "./main.py"]