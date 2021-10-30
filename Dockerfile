FROM python:3.10-alpine
LABEL org.opencontainers.image.source https://github.com/qernal/github-actions-assets

# add packages
RUN apk add curl openssl-dev libffi-dev git gcc musl-dev make --no-cache
COPY ./src /

# install pip requirements
RUN pip install -r requirements.txt

CMD ["python", "/assets.py"]