
from utils.db import run_schema
from utils.logger import setup_logger

from generators.organizations import generate_organization
from generators.users import generate_users
from generators.teams import generate_teams
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.custom_fields import generate_custom_fields
from generators.custom_field_values import generate_custom_field_values
from generators.comments import generate_comments
from generators.task_followers import generate_task_followers
from utils.validation import run_validations


def main():
    logger = setup_logger()

    logger.info("Initializing database")
    conn = run_schema()   # ✅ SAFE on Windows

    logger.info("Creating organization")
    org_id = generate_organization(conn)

    logger.info("Creating users")
    user_ids = generate_users(conn, org_id, 5000)

    logger.info("Creating teams")
    team_ids = generate_teams(conn, org_id, user_ids)

    logger.info("Creating projects")
    project_ids = generate_projects(conn, org_id, team_ids, user_ids)

    logger.info("Creating sections")

    generate_sections(conn, project_ids)

    logger.info("Creating tasks")
    task_ids = generate_tasks(conn, org_id, project_ids, user_ids)

    logger.info("Creating custom fields")
    field_ids, option_map = generate_custom_fields(
        conn, org_id, user_ids, project_ids)

    logger.info("Assigning custom field values")
    generate_custom_field_values(conn, task_ids, field_ids, option_map)

    logger.info("Generating comments")
    generate_comments(conn, task_ids, user_ids)

    logger.info("Generating task followers")
    generate_task_followers(conn, task_ids, user_ids)

    logger.info("Running data validations")
    run_validations(conn)

    conn.commit()
    conn.close()

    logger.info("Database generation completed successfully")


if __name__ == "__main__":
    main()
