import uuid
import random
from utils.faker_utils import fake_name
from utils.time_utils import random_past_date


def generate_users(conn, org_id, n_users=5000):
    users = []
    user_ids = []
    used_emails = set()

    for _ in range(n_users):
        uid = str(uuid.uuid4())
        name = fake_name()

        base = name.lower().replace(" ", ".")
        email = f"{base}@acme.com"
        counter = 1
        while email in used_emails:
            email = f"{base}{counter}@acme.com"
            counter += 1
        used_emails.add(email)

        is_admin = random.random() < 0.03
        role = "member"

        is_active = random.random() < 0.9
        created_at = random_past_date(days=365)

        last_login = None
        if is_active:
            last_login = random_past_date(days=30)

        users.append((
            uid,
            org_id,
            name,
            email,
            role,
            is_admin,
            is_active,
            created_at,
            last_login
        ))

        user_ids.append(uid)

    conn.executemany("""
        INSERT INTO users
        (user_id, organization_id, name, email, role,
         is_admin, is_active, created_at, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, users)

    return user_ids
