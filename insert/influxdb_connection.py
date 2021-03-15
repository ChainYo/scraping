from influxdb_client import InfluxDBClient, Point, WriteOptions
from dotenv import load_dotenv
import json
import os

class DB():

    # Method to open connection
    @classmethod
    def open_con(cls):
        load_dotenv()
        cls.token = os.getenv('INFLUXDB_V2_TOKEN')
        cls.org = os.getenv('INFLUXDB_V2_ORG')
        cls.bucket = os.getenv('INFLUXDB_V2_BUCKET')
        cls.url = "http://influxdb:8086"
        cls.client = InfluxDBClient(url=cls.url, token=cls.token, org=cls.org)
        print('Connected')
        cls.write_api = cls.client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000, jitter_interval=2_000, retry_interval=5_000, max_retries=5, max_retry_delay=30_000, exponential_base=2))

    # Method to close connection
    @classmethod
    def close_con(cls):
        cls.client.close()

    # Method to insert JSON
    @classmethod
    def insert_json(cls, file):
        cls.open_con()
        with open(file) as f:
            file_data = json.load(f)
        cls.write_api.write(bucket=cls.bucket, org=cls.org, record=file_data)
        cls.close_con()
        print(f'Json inséré')
