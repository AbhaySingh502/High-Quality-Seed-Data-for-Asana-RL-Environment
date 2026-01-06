import uuid
import random
from utils.faker_utils import fake_sentence


def generate_comments(conn, task_ids, user_ids):
    comments = []

    for tid in task_ids:
        for _ in range(random.randint(0, 4)):
            comments.append((
                str(uuid.uuid4()),
                tid,
                random.choice(user_ids),
                fake_sentence(),
                False
            ))

    conn.executemany("""
        INSERT INTO comments
        (comment_id, task_id, user_id, content, is_system_generated)
        VALUES (?, ?, ?, ?, ?)
    """, comments)
