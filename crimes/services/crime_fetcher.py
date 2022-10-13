from google.cloud import bigquery
from threading import Thread

from crimes.models import Crime


class CrimesFetcherJob:
    BATCH_SIZE = 2000
    THREAD_COUNT = 10
    CRIME_FIELDS = ['unique_key', 'primary_type', 'description', 'date', 'latitude', 'longitude']

    def __init__(self):
        self.client = bigquery.Client()
        self.total_crimes_count = 0

    def run(self):
        self._fetch_crimes_count()
        threads = [Thread(target=self._run_worker, args=(thread_idx,))
                   for thread_idx in range(self.THREAD_COUNT)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def _fetch_crimes_count(self):
        QUERY = 'SELECT COUNT(*) FROM `bigquery-public-data.chicago_crime.crime`'
        self.total_crimes_count = list(enumerate(self.client.query(QUERY).result()))[0][1][0]

    def _run_worker(self, worker_idx: int):
        batch_idx_start = (worker_idx * (self.total_crimes_count // self.THREAD_COUNT)) // self.BATCH_SIZE
        batch_idx_end = ((worker_idx + 1) * (self.total_crimes_count // self.THREAD_COUNT)) // self.BATCH_SIZE

        for batch_idx in range(batch_idx_start, batch_idx_end):
            batch_result = self._fetch_batch(batch_idx)
            crimes = []
            crime_infos = [item
                           for item in batch_result
                           if (item.latitude and item.longitude)]

            for crime_info in crime_infos:
                crime = Crime()
                for field in self.CRIME_FIELDS:
                    setattr(crime, field, getattr(crime_info, field))
                crimes.append(crime)
            Crime.objects.bulk_create(crimes, ignore_conflicts=True)

    def _fetch_batch(self, batch_idx: int):
        QUERY = f'''
                    SELECT * FROM `bigquery-public-data.chicago_crime.crime`  
                    ORDER BY unique_key ASC 
                    LIMIT {self.BATCH_SIZE} OFFSET {self.BATCH_SIZE * batch_idx} 
                '''
        return self.client.query(QUERY).result()
