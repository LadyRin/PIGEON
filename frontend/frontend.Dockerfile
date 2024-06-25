FROM httpd:2.4
COPY . /app

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nodejs npm && \
    apt-get clean

RUN npm install && \
    npm run build

RUN cp -r /app/dist/* /usr/local/apache2/htdocs/

EXPOSE 80

ENTRYPOINT ["httpd-foreground"]

