FROM ubuntu:latest

EXPOSE 80
WORKDIR /app

ENV LANG=C.UTF-8

# installing deps

RUN apt-get update
RUN apt-get install -y supervisor python3 python3-pip ipset iptables sudo nginx

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY langate2000-supervisor.conf /etc/supervisor/supervisord.conf

# nginx setup

COPY langate2000-nginx.conf /etc/nginx/sites-enabled/default
RUN mkdir -p /var/www/html/static

# Django setup

ADD langate /app/langate
ADD langate2000-networkd /app/langate2000-networkd

WORKDIR /app/langate/

#RUN export secret_key=$(pwgen -1 -n 100) && sed "s/<generated_random_key>/$secret_key/" langate/settings_local.py.template > langate/settings_local.py

RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py makemigrations --noinput
RUN python3 manage.py migrate --noinput
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', '', 'rien')" | python3 manage.py shell

CMD [ "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]
