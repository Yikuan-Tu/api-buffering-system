import logging
from collections import deque
from typing import Deque, List
from app.models import Person
from app.utils.config import BUFFER_SIZE
from app.utils.database import batch_insert, execute_query

logger = logging.getLogger(__name__)

buffer: Deque[Person] = deque(maxlen=BUFFER_SIZE)


def flush_to_db():
    if not buffer:
        return

    records = [(p.first_name, p.last_name) for p in buffer]
    try:
        inserted = batch_insert(records)
        logger.info(f"Flushed {inserted} records to database")
        logger.info(f"✅ Successfully flushed {len(buffer)} records to database")
        buffer.clear()
        return execute_query("SELECT COUNT(*) FROM people")
    except Exception as e:
        logger.error(f"❌ Flush failed: {str(e)}")
        raise e


def buffer_data(people: List[Person]):
    buffer.extend(people)

    if len(buffer) >= BUFFER_SIZE:
        logger.info("\n=== FLUSH TRIGGERED ===")
        logger.info(f"Flushing {len(buffer)} records to database...")
        return flush_to_db()
    return len(buffer)
