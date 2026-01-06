import uuid
import random
from utils.time_utils import random_past_date, random_future_date

PROJECT_NAMES = [
    "Website Revamp", "Mobile App v2", "Data Platform Migration",
    "Customer Retention Initiative", "SEO Campaign", "Infra Cost Optimization"
]


def generate_projects(conn, org_id, team_ids, user_ids, n_projects=60):
    projects = []

    for _ in range(n_projects):
        pid = str(uuid.uuid4())
        projects.append((
            pid,
            org_id,
            random.choice(team_ids),
            random.choice(PROJECT_NAMES),
            random.choice(user_ids),
            random_past_date(),
            random_future_date()
        ))

    conn.executemany("""
        INSERT INTO projects
        (project_id, organization_id, team_id, name, owner_id, start_date, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, projects)

    return [p[0] for p in projects]
