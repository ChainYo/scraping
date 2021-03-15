from time import sleep
from os import listdir, remove
from os.path import isfile, join

from influxdb_connection import DB

while True:
    json_files = [f for f in listdir('app/json_files') if isfile(join('app/json_files', f))]
    for file in json_files:
        DB.insert_json(f"app/json_files/{file}")
        remove(f"app/json_files/{file}")
        print(f'File removed: {file}')
    sleep(300)
