'''
Script for retrieving weather data via OpenWeatherMap API
    • api_key_1 = 'f8fb4a57826b52cf7a7bf5225eaec506'
    • api_key_2 = 'a0b65bac25867383266ad37aa1373f4d'
Pre-requisites:
    • minio/mc: for AWS S3 connection. You will need access key and secret key.
    • pytz
'''

# city & id list
location = ['Sapporo', 'Sendai', 'Niigata', 'Tokyo', 'Nagoya', 'Osaka', 'Hiroshima', 'Kochi', 'Fukuoka', 'Miyazaki', 'Naha']
loc_id = [2128295, 2111149, 1855431, 1850147, 1856057, 1853909, 1862415, 1859146, 1863967, 1856717, 1856035]

from datetime import datetime
from pytz import timezone
import requests
import pytz
import json, glob, os


def weather_get(id):
    key = 'f8fb4a57826b52cf7a7bf5225eaec506'
    api = 'http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}'
    url = api.format(id, key)
    response = requests.get(url)
    data = json.loads(response.text)
    # convert UTC time to Asia/Tokyo (human readable)
    dt_obj = datetime.fromtimestamp(int(data['dt']))
    dt_jp = pytz.utc.localize(dt_obj, is_dst=None).\
                    astimezone(pytz.timezone('Asia/Tokyo'))
    dt = dt_jp.strftime('%Y-%m-%d %H:%M:%S')
    # replace datetime with local datetime
    data['dt'] = dt
    return dt, data

def dump(city, dt, data):
    month = dt[:(dt.index('-') + 3)].replace('-', '')
    hour = dt[:dt.index(':')] + '時'
    try:
        with open ('{}/{}/{}.json'.format(ab_path, city, month), 'r', encoding='utf-8') as f:
            temp_json = json.load(f)
            if hour not in temp_json:
                temp_json[hour] = data
            # else: don't change anything
        with open ('{}/{}/{}.json'.format(ab_path, city, month), 'w', encoding='utf-8') as f1:
            json.dump(temp_json, f1)
    except FileNotFoundError as e:
        with open ('{}/{}/{}.json'.format(ab_path, city, month), 'w', encoding='utf-8') as f2:
            temp_json = {}
            temp_json[hour] = data
            json.dump(temp_json, f2)

def main():
    # check if city folders exist
    folders = glob.glob(ab_path+'/*/')
    names = [x.replace(ab_path, '').replace('/', '') for x in folders]
    if sorted(names) != sorted(location):
        print ('Folders don\'t exist! Creating folders...')
        for i in location:
            os.system('mkdir {}/{}'.format(ab_path,i))
        print ('Finished creating folders. Now start api...\n...')
    # start api...
    for id in loc_id:
        dt, data = weather_get(id)
        city = location[loc_id.index(id)]
        print ('Now city: ', city)
        dump(city, dt, data)
    print ('...\nDone.')

if __name__ == '__main__':
    ab_path = '/home/irep/sdb/work/weather_cron'
    main()
