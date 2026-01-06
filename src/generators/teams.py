import uuid
import random

TEAM_NAMES = [
    "Backend Engineering", "Frontend Engineering", "Data Science",
    "Product Management", "Marketing", "Operations", "QA"
]


def generate_teams(conn, org_id, user_ids):
    teams = []
    memberships = []

    for name in TEAM_NAMES:
        team_id = str(uuid.uuid4())
        teams.append((team_id, org_id, name))

        members = random.sample(user_ids, k=random.randint(10, 50))
        for uid in members:
            memberships.append((team_id, uid, "member"))

    conn.executemany("""
        INSERT INTO teams (team_id, organization_id, name)
        VALUES (?, ?, ?)
    """, teams)

    conn.executemany("""
        INSERT INTO team_members (team_id, user_id, role_in_team)
        VALUES (?, ?, ?)
    """, memberships)

    return [t[0] for t in teams]
