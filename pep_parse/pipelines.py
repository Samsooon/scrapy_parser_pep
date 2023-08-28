from itemadapter import ItemAdapter
from pathlib import Path
import csv

from .settings import NOW_TIME

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.__status_vocabulary = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status'):
            pep_status = adapter['status']
            self.__status_vocabulary[pep_status] = (
                self.__status_vocabulary.get(pep_status, 0) + 1
            )
            return item

    def close_spider(self, spider):
        SAVES_DIR = BASE_DIR / 'results'
        filename = 'status_summary_' + NOW_TIME + '.csv'
        with open(SAVES_DIR / filename, mode='w', encoding='utf-8') as file:
            csv.writer(
                file, dialect=csv.unix_dialect, quoting=csv.QUOTE_NONE
            ).writerows(
                (
                    ('Статус', 'Количество'),
                    *self.__status_vocabulary.items(),
                    ('Total', sum(self.__status_vocabulary.values()))
                )
            )
