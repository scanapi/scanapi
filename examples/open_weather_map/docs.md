
## Request: GET http://api.openweathermap.org/data/2.5/weather?APPID=<YOUR_API_KEY>&q=Rio+de+Janeiro

HEADERS:
<details><summary></summary><p>

```
{
  "User-Agent": "python-requests/2.22.0",
  "Accept-Encoding": "gzip, deflate",
  "Accept": "*/*",
  "Connection": "keep-alive",
  "Content-Length": "2",
  "Content-Type": "application/json"
}
```
</p></details>

### Response: 200

Is redirect? False

HEADERS:
<details><summary></summary><p>

```
{
  "Server": "openresty",
  "Date": "Mon, 05 Aug 2019 20:25:55 GMT",
  "Content-Type": "application/json; charset=utf-8",
  "Content-Length": "472",
  "Connection": "keep-alive",
  "X-Cache-Key": "/data/2.5/weather?APPID=<YOUR_API_KEY>&q=rio+de+janeiro",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Credentials": "true",
  "Access-Control-Allow-Methods": "GET, POST"
}
```
</p></details>

Content:
<details><summary></summary><p>

```
{
  "coord": {
    "lon": -43.21,
    "lat": -22.91
  },
  "weather": [
    {
      "id": 521,
      "main": "Rain",
      "description": "shower rain",
      "icon": "09d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 294.01,
    "pressure": 1029,
    "humidity": 88,
    "temp_min": 292.15,
    "temp_max": 296.15
  },
  "visibility": 10000,
  "wind": {
    "speed": 6.2,
    "deg": 80
  },
  "clouds": {
    "all": 75
  },
  "dt": 1565035993,
  "sys": {
    "type": 1,
    "id": 8429,
    "message": 0.0054,
    "country": "BR",
    "sunrise": 1564997087,
    "sunset": 1565037175
  },
  "timezone": -10800,
  "id": 3451190,
  "name": "Rio de Janeiro",
  "cod": 200
}
```
</p></details>
