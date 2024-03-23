# CloudFlareUpdater

Скрипт для автоматического обновления динамического ip адреса в указаных DNS записях в CloudFlare.

## Конфигурация:

Для настройки скрипта создайте в папке возле `main.py` файл `config.json` со следующим содержимым:
```JSON
{
  "log_file_name": "updater.log",
  "email": "your_email@gmail.com",
  "token_key": "your_cloudflare_api_key",
  "zones": [
    {
      "name": "zone.com",
      "domains": [
        "zone.com",
        "subdomain.zone.com"
      ]
    }
  ],
  "refresh_interval": 300
}
```
* `"log_file_name"(optional)`: Файл, куда будут сохраняться логи обновлений IP. Если не указать - логи выводятся в консоль
* `"email"`: Ваш email от аккаунта CloudFlare
* `"token_key"`: Ваш API token в аккаунте CloudFlare([Как получить](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/))
* `"zones"`: Список зон, домены в которых нужно обновлять
  * `"name"`: Название зоны
  * `"domains"`: Список доменов для обновления в данной зоне
* `"refresh_interval"`: Время в секундах

## Запуск
После создания конфигурационного файла просто запустите файл `main.py` и добавьте его в автозагрузку
