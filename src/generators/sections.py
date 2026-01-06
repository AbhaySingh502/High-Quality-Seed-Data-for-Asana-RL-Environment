import uuid

DEFAULT_SECTIONS = ["Backlog", "To Do", "In Progress", "Review", "Done"]


def generate_sections(conn, project_ids):
    sections = []

    for pid in project_ids:
        for i, name in enumerate(DEFAULT_SECTIONS):
            sections.append((str(uuid.uuid4()), pid, name, i))

    conn.executemany("""
        INSERT INTO sections (section_id, project_id, name, order_index)
        VALUES (?, ?, ?, ?)
    """, sections)
