from datetime import datetime, timedelta
import random


def random_past_date(days=180):
    return datetime.now() - timedelta(days=random.randint(1, days))


def random_future_date(days=90):
    return datetime.now() + timedelta(days=random.randint(1, days))
