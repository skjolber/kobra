# Alpine is preferred, but Oracle only works with glibc.
FROM alpine:3.4

RUN mkdir /src
WORKDIR /src

ENV NODE_ENV=production \
    DJANGO_SETTINGS_MODULE=kobra.settings.production \
    PYTHONPATH=/src:$PYTHONPATH \
    PYTHONUNBUFFERED=true

ADD ./requirements.alpine /src/requirements.alpine
RUN apk add --no-cache $(grep -vE "^\s*#" /src/requirements.alpine | tr "\n" " ") && \
    ln -sf /usr/bin/python3 /usr/bin/python

ADD ./requirements.pip /src/requirements.pip
RUN pip3 install -U pip setuptools && pip3 install -r /src/requirements.pip

ADD ./package.json /src/package.json
RUN npm install

ADD . /src

RUN npm run build && \
    DJANGO_SECRET_KEY=build DJANGO_DATABASE_URL=sqlite://// django-admin collectstatic --no-input
CMD ["/src/run-django.sh"]
EXPOSE 8000
