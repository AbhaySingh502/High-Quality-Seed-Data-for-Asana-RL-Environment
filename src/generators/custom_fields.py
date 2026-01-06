import uuid
import random

CUSTOM_FIELDS = [
    ("Priority", "enum", ["Low", "Medium", "High", "Critical"]),
    ("Effort Estimate", "number", None),
    ("Customer Impact", "enum", ["Low", "Medium", "High"]),
    ("Release Version", "text", None),
    ("Requires Approval", "boolean", None)
]


def generate_custom_fields(conn, org_id, user_ids, project_ids):
    field_ids = []
    option_map = {}

    for name, ftype, options in CUSTOM_FIELDS:
        field_id = str(uuid.uuid4())
        field_ids.append(field_id)

        conn.execute("""
            INSERT INTO custom_fields
            (field_id, organization_id, name, type, is_global, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (field_id, org_id, name, ftype, True, random.choice(user_ids)))

        if options:
            option_map[field_id] = []
            for idx, opt in enumerate(options):
                opt_id = str(uuid.uuid4())
                option_map[field_id].append(opt_id)

                conn.execute("""
                    INSERT INTO custom_field_options
                    (option_id, field_id, value, sequence)
                    VALUES (?, ?, ?, ?)
                """, (opt_id, field_id, opt, idx))

    # Attach fields to projects
    for pid in project_ids:
        for fid in field_ids:
            conn.execute("""
                INSERT INTO project_custom_fields
                (project_id, field_id, required, field_order)
                VALUES (?, ?, ?, ?)
            """, (pid, fid, random.random() < 0.3, random.randint(1, 10)))

    return field_ids, option_map
