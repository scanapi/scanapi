
## Request: GET http://api.openweathermap.org/data/2.5/weather?APPID=<YOUR_API_KEY>&q=Rio+de+Janeiro

HEADERS:
<details><summary></summary><p>

```
{
  "User-Agent": "python-requests/2.22.0",
  "Accept-Encoding": "gzip, deflate",
  "Accept": "*/*",
  "Connection": "keep-alive"
}
```
</p></details>

BODY:
None

### Response: 200

Is redirect? False

HEADERS:
<details><summary></summary><p>

```
{
  "Server": "openresty",
  "Date": "Thu, 01 Aug 2019 20:46:38 GMT",
  "Content-Type": "application/json; charset=utf-8",
  "Content-Length": "471",
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
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 298.49,
    "pressure": 1013,
    "humidity": 78,
    "temp_min": 295.37,
    "temp_max": 302.15
  },
  "visibility": 10000,
  "wind": {
    "speed": 5.7,
    "deg": 180
  },
  "clouds": {
    "all": 0
  },
  "dt": 1564692144,
  "sys": {
    "type": 1,
    "id": 8429,
    "message": 0.0063,
    "country": "BR",
    "sunrise": 1564651618,
    "sunset": 1564691475
  },
  "timezone": -10800,
  "id": 3451190,
  "name": "Rio de Janeiro",
  "cod": 200
}
```
</p></details>
