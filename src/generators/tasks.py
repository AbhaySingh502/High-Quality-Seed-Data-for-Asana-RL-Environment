import uuid
import random
from datetime import timedelta
from utils.time_utils import random_past_date, random_future_date

TASK_TITLES = [
    "Implement API",
    "Fix login bug",
    "Design database schema",
    "Optimize query performance",
    "Prepare release notes",
    "Set up monitoring"
]


def generate_tasks(conn, org_id, project_ids, user_ids, n_tasks=20000):
    tasks = []
    task_projects = []
    task_ids = []

    now = random_past_date(days=1)

    for _ in range(n_tasks):
        tid = str(uuid.uuid4())
        task_ids.append(tid)

        created_at = random_past_date(days=180)
        due_date = created_at + timedelta(days=random.randint(3, 45))

        # Completion logic
        is_completed = random.random() < 0.7
        completed_at = None

        if is_completed:
            completed_at = created_at + timedelta(days=random.randint(1, 30))
            if completed_at > now:
                completed_at = None
                is_completed = False

        assignee = random.choice(user_ids) if random.random() > 0.15 else None

        tasks.append((
            tid,
            org_id,
            random.choice(TASK_TITLES),
            assignee,
            random.choice(user_ids),
            created_at,
            due_date,
            is_completed,
            completed_at
        ))

        for pid in random.sample(project_ids, k=random.randint(1, 2)):
            task_projects.append((tid, pid))

    conn.executemany("""
        INSERT INTO tasks
        (task_id, organization_id, title, assignee_id, creator_id,
         created_at, due_date, is_completed, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tasks)

    conn.executemany("""
        INSERT INTO task_projects (task_id, project_id)
        VALUES (?, ?)
    """, task_projects)

    return task_ids
