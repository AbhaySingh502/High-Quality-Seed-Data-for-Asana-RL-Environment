import uuid
import random


def generate_custom_field_values(conn, task_ids, field_ids, option_map):
    rows = []

    for tid in task_ids:
        for fid in field_ids:
            if random.random() < 0.7:  # not all tasks have all fields
                value_text = value_number = value_date = value_boolean = option_id = None

                if fid in option_map:
                    option_id = random.choice(option_map[fid])
                else:
                    value_number = round(random.uniform(1, 20), 1)

                rows.append((
                    str(uuid.uuid4()), tid, fid,
                    option_id, value_text, value_number, value_date, value_boolean
                ))

    conn.executemany("""
        INSERT INTO task_custom_field_values
        (id, task_id, field_id, option_id,
         value_text, value_number, value_date, value_boolean)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
