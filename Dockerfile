FROM node:lts AS build-frontend

WORKDIR /src/theme
COPY ./theme /src/theme

RUN npm install
RUN npm run build


FROM python:3.9-bookworm

WORKDIR /usr/src/app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY --from=build-frontend /src/static ./static

EXPOSE 8000

CMD ["bash", "run.sh"]
