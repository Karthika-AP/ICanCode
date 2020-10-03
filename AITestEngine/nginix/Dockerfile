FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./ssl/ /etc/nginx/ssl/

COPY ./AITestEngine/nginix/nginx.conf /etc/nginx/

COPY ./AITestEngine/nginix/docker_nginix.conf /etc/nginx/sites-available/

COPY ./AITestEngine/nginix/docker_nginix.conf /etc/nginx/conf.d/



