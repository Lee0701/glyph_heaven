FROM node:lts AS build-frontend

WORKDIR /src/theme
COPY ./theme /src/theme

RUN npm install
RUN npm run build


FROM python:3.9-bookworm AS build-kage-data

workdir /src

COPY cvt_glyphwiki_data.py .
COPY dump_newest_only.txt .
RUN python cvt_glyphwiki_data.py


FROM python:3.9-bookworm

WORKDIR /usr/src/app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY --from=build-frontend /src/static ./static
COPY --from=build-kage-data /src/kage.tsv .

EXPOSE 8000

CMD ["bash", "run.sh"]
