# Telegram bot 
Bot - interaction with the service [django_service_anime](https://github.com/OleksiiMartseniuk/django_service_anime)

#### Actions
* Receiving schedules
* Timeline
* Search by name
* Receiving anons
* Filter by genre

#### Admin
* Collection of user statistics

#### Technology
* Python => 3.10
* Aiogram
* Httpx

#### Test
`docker exec -it bot bash`
* Pytest `pytest tests`
#### Instructions

Create a file at the root of the project `.env`

```
# Bot
export TOKEN_BOT='you_token'

# TimeZone
export TZ='you_time_zone'

# Api
export API_KEY='you_api_key'
```
