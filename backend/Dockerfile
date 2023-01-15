FROM python:3.8-slim
RUN python3 -m pip install --upgrade pip
COPY ../data .
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
ONBUILD RUN python manage.py migrate
ONBUILD RUN python manage.py collectstatic --noinput
