import uuid


def generate_organization(conn):
    org_id = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO organizations (organization_id, name, domain)
        VALUES (?, ?, ?)
    """, (org_id, "Acme SaaS Corp", "acme.com"))
    return org_id
