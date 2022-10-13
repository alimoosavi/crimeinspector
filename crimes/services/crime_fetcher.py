from google.api_core.exceptions import GoogleAPICallError
from concurrent.futures import TimeoutError
from google.cloud import bigquery
from threading import Thread , Lock
from typing import Tuple
from crimes.models import Crime
from logging import getLogger

logger = getLogger('main')


class CrimesFetcherJob:
    '''
        CrimesFetcherJob fetches and persists criminal data by using multi-threads
    '''
    BATCH_SIZE = 2000
    THREAD_COUNT = 10
    GOOGLE_BIG_QUERY_DATASET = 'bigquery-public-data.chicago_crime.crime'
    CRIME_FIELDS = ['unique_key', 'primary_type', 'description', 'date', 'latitude', 'longitude']

    def __init__(self):
        self.client = bigquery.Client()
        self.lock = Lock()
        self.total_crimes_count = 0

    def run(self):
        if not self._fetch_crimes_total_count():
            return

        threads = [Thread(target=self._run_worker, args=(thread_idx,))
                   for thread_idx in range(self.THREAD_COUNT)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def _fetch_crimes_total_count(self) -> bool:
        logger.info('Fetching total count of crimes')
        QUERY = f'SELECT COUNT(*) FROM `{self.GOOGLE_BIG_QUERY_DATASET}`'
        try:
            result = self.client.query(QUERY).result()
        except (GoogleAPICallError, TimeoutError):
            logger.error('Fetching total count of crimes has failed!')
            return False

        self.total_crimes_count = list(enumerate(result))[0][1][0]
        logger.info('Total count of crimes has been fetched successfully')
        return True

    @classmethod
    def _get_worker_batch_idx_range(cls, worker_idx: int, total_crimes_count: int) -> Tuple[int, int]:
        return ((worker_idx * (total_crimes_count // cls.THREAD_COUNT)) // cls.BATCH_SIZE,
                ((worker_idx + 1) * (total_crimes_count // cls.THREAD_COUNT)) // cls.BATCH_SIZE,)

    def _run_worker(self, worker_idx: int):
        """
            This method fetches part of dataset corresponds to worker_idx chunk by chunk and persist them
            using bulk_create api of django orm to the database
        :param worker_idx:
                specifies index of worker (thread)
        :return:
        """
        batch_idx_start, batch_idx_end = self._get_worker_batch_idx_range(worker_idx, self.total_crimes_count)

        for batch_idx in range(batch_idx_start, batch_idx_end):
            batch_result = self._fetch_batch(batch_idx)
            if not batch_result:
                logger.error(f'batch_idx:{batch_idx} of worker_idx: {worker_idx} has failed to be fetched')
                continue

            crimes = []
            crime_infos = [item
                           for item in batch_result
                           if (item.latitude and item.longitude)]

            for crime_info in crime_infos:
                crime = Crime()
                for field in self.CRIME_FIELDS:
                    setattr(crime, field, getattr(crime_info, field))
                crimes.append(crime)

            self.lock.acquire()
            Crime.objects.bulk_create(crimes, ignore_conflicts=True)
            self.lock.release()

            if batch_idx % 10 == 0:
                logger.info(f'worker_idx:{worker_idx} passed batch_idx:{batch_idx}')
                
    def _fetch_batch(self, batch_idx: int):
        """
            fetches chunk of data corresponding to batch_idx
        :param batch_idx (int):
                specifies index of the batch
        :return:
                google.cloud.bigquery.table.RowIterator:
                    Iterator of row data
        """

        QUERY = f'''
                    SELECT * FROM `{self.GOOGLE_BIG_QUERY_DATASET}`  
                    ORDER BY unique_key ASC 
                    LIMIT {self.BATCH_SIZE} OFFSET {self.BATCH_SIZE * batch_idx} 
                '''

        try:
            return self.client.query(QUERY).result()
        except (GoogleAPICallError, TimeoutError):
            return None
