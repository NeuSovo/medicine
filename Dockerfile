FROM alang/django
ENV DJANGO_APP=medicine 
COPY . /usr/django/app
ENV DJANGO_MANAGEMENT_ON_START='collectstatic --noinput';'migrate --noinput';'loaddata info.json'
ENV USE_MYSQL=false MYSQL_PASSWORD=123456 MYSQL_PORT=3306 MYSQL_HOST=127.0.0.1 RELEASE=false
RUN pip install -r /usr/django/app/requirements.txt
