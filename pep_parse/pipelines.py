from collections import defaultdict
from itemadapter import ItemAdapter
from pathlib import Path
import csv

from .settings import NOW_TIME

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.__pep_statuses = defaultdict(int)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('status'):
            self.__pep_statuses[adapter['status']] += 1
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
                    *self.__pep_statuses.items(),
                    ('Total', sum(self.__pep_statuses.values()))
                )
            )
