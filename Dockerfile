FROM --platform=$BUILDPLATFORM python:3-alpine

ARG TARGETPLATFORM
ARG BUILDPLATFORM

ENV COOKIE_FILE=/run/secrets/cookie.json
ENV BOT_TOKEN_FILE=/run/secrets/bot_token.txt

WORKDIR /app
COPY . /app
RUN python3 -m pip install EdgeGPT --upgrade \
    pip install -r requirements.txt && \
    pip install aiohttp pyTelegramBotAPI

CMD ["python", "bingbot.py"]