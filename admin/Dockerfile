FROM python:3.8.5

COPY ./admin /admin/
COPY ./.env /

COPY ./requirements.txt /
RUN pip install -r requirements.txt
RUN pip install pydantic[dotenv]

EXPOSE 8000

WORKDIR /admin

CMD ["python", "main.py"]
