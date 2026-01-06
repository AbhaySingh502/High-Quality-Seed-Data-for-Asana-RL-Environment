import random


def generate_task_followers(conn, task_ids, user_ids):
    followers = []

    for tid in task_ids:
        for uid in random.sample(user_ids, k=random.randint(0, 5)):
            followers.append((tid, uid))

    conn.executemany("""
        INSERT INTO task_followers (task_id, user_id)
        VALUES (?, ?)
    """, followers)
