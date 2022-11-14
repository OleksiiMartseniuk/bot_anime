<p align="center">
      <img src="https://i.ibb.co/nQKkFXM/telegram-icon.png" width="200">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/Python-3.10.6-blue" alt="Python">
   <img src="https://img.shields.io/badge/Framework-Aiogram%202.21-blueviolet" alt="Framework">
   <img src="https://img.shields.io/badge/Version-v1.0-blue" alt=" Version">
   <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License">
</p>

## About

Telegram bot that allows you to interact with the service [DjangoServiceAnime](https://github.com/OleksiiMartseniuk/django_service_anime). Subscribe to anime and get notified when a new series is released. Display information about anime.

## Documentation

### Telegram commands

|Commands|Descriptions|
|-------|--------|
|*`/profile`*|Subscribe to anime and get a reminder when a new series is released|
|*`/schedules`*|Anime release schedule sorted by day of the week|
|*`/timeline`*|Latest updated anime without a release date|
|*`/anons`*|Receive announcements|
|*`/search`*|Search anime by name|
|*`/filter_genre`*|Filter by genre|
|*`/about`*|Information about the bot, the ability of the user to send messages to the administrator|
|*`/cancel`*|Cancel current action|

### Technology

![Python](https://img.shields.io/badge/-Python-blue?style=flat-square)
![Aiogram](https://img.shields.io/badge/-Aiogram-success?style=flat-square)
![Httpx](https://img.shields.io/badge/-Httpx-blueviolet?style=flat-square)

### Instructions

Create a file at the root of the project `.env`

```
# Bot
export TOKEN_BOT='you_token'

# TimeZone
export TZ='you_time_zone'

# Api
export API_KEY='you_api_key'
export HOST_API='host_django_service_anime'
```

Build the image and run the container

```bash
docker-compose up --build
```


### Test

```bash
docker exec -it bot bash
```

Pytest

```bash
pytest tests
```

## Distribute

- [@anime_schedules_bot](https://t.me/anime_schedules_bot)

## Developers

- [Martseniuk Oleksii](https://github.com/OleksiiMartseniuk)

## License

Project AnimeBot is distributed under the MIT license.
