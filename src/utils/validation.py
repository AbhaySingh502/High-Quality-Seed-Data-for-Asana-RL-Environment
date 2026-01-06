def run_validations(conn):
    cursor = conn.cursor()

    # 1. completed_at must be after created_at
    cursor.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE completed_at IS NOT NULL
        AND completed_at < created_at
    """)
    assert cursor.fetchone()[0] == 0, "Invalid completion timestamps"

    # 2. completed tasks must be marked completed
    cursor.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE completed_at IS NOT NULL
        AND is_completed = 0
    """)
    assert cursor.fetchone()[0] == 0, "Completion flag mismatch"

    # 3. Tasks must belong to at least one project
    cursor.execute("""
        SELECT COUNT(*) FROM tasks t
        LEFT JOIN task_projects tp ON t.task_id = tp.task_id
        WHERE tp.project_id IS NULL
    """)
    assert cursor.fetchone()[0] == 0, "Task without project found"

    print("✅ Data validation passed")
