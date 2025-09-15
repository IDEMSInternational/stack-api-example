FROM stackmaths/stackapi:2024072400-latest AS builder
WORKDIR /opt/idems
RUN apt update \
 && apt install --yes --no-install-recommends apache2-dev git
RUN git clone --depth 1 https://github.com/danghvu/mod_dumpost.git
RUN cd mod_dumpost && make && apxs -i -A -n dumpost mod_dumpost.la

FROM stackmaths/stackapi:2024072400-latest
ENV DUMP_POST_MAX_SIZE=256000 \
    STACK_LOG_LEVEL=info
COPY --from=builder /usr/lib/apache2/modules/mod_dumpost.so /usr/lib/apache2/modules/
COPY --from=builder /etc/apache2/mods-available/dumpost.load /etc/apache2/mods-available/
RUN a2enmod dumpost
RUN a2enmod headers
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
