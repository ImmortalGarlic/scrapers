### OpenWeatherMap API 経由で気象情報の取得スクリプト

#### Pre-requisites
- Python3
- requests
- pytz
- minio/mc

#### 使い方
``` $ python3 openweather.py ```

#### 保存構造（月単位のjson）
```markdown
|----openweather.py
|----Fukuoka
        |----201709.json
        |----201710.json
        |----201711.json
|----Tokyo
        |----201709.json
        |----201710.json
        |----201711.json
....
```

#### Linux crontab command（例）
```
# auto weather data retriever for openweathermap

PYTHONIOENCODING = 'utf-8'
0,30 * * * * /usr/bin/python3 /home/ubuntu/sdb/work/weather_cron/openweather.py
15,45 * * * * /home/ubuntu/plugins/mc mirror /home/ubuntu/sdb/work/weather_cron/ s3/openweathermap/
```
