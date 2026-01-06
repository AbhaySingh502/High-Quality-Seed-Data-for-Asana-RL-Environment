PRAGMA foreign_keys = ON;

-- =========================
-- ORGANIZATIONS
-- =========================
CREATE TABLE organizations (
    organization_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK (role IN ('member', 'guest', 'limited_member')),
    is_admin BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- =========================
-- TEAMS
-- =========================
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- =========================
-- TEAM MEMBERS
-- =========================
CREATE TABLE team_members (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role_in_team TEXT CHECK (role_in_team IN ('admin', 'member')),
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- PROJECTS
-- =========================
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    team_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    due_date DATE,
    status TEXT CHECK (status IN ('active', 'completed', 'archived')),
    archived BOOLEAN DEFAULT 0,
    owner_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- =========================
-- SECTIONS
-- =========================
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- =========================
-- TASKS
-- =========================
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    creator_id TEXT NOT NULL,
    parent_task_id TEXT,
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    status TEXT CHECK (status IN ('todo', 'in_progress', 'done')),
    start_date DATE,
    due_date DATE,
    is_completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (creator_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id)
);

-- =========================
-- TASK ↔ PROJECT (Multi-homing)
-- =========================
CREATE TABLE task_projects (
    task_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    PRIMARY KEY (task_id, project_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- =========================
-- TASK FOLLOWERS
-- =========================
CREATE TABLE task_followers (
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    PRIMARY KEY (task_id, user_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- COMMENTS
-- =========================
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    is_system_generated BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- TAGS
-- =========================
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- =========================
-- TASK ↔ TAGS
-- =========================
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- =========================
-- CUSTOM FIELDS
-- =========================
CREATE TABLE custom_fields (
    field_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('text', 'number', 'date', 'boolean', 'enum')),
    is_global BOOLEAN DEFAULT 0,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- =========================
-- PROJECT CUSTOM FIELDS
-- =========================
CREATE TABLE project_custom_fields (
    project_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    required BOOLEAN DEFAULT 0,
    field_order INTEGER,
    PRIMARY KEY (project_id, field_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (field_id) REFERENCES custom_fields(field_id)
);

-- =========================
-- CUSTOM FIELD OPTIONS
-- =========================
CREATE TABLE custom_field_options (
    option_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    value TEXT NOT NULL,
    sequence INTEGER,
    FOREIGN KEY (field_id) REFERENCES custom_fields(field_id)
);

-- =========================
-- TASK CUSTOM FIELD VALUES
-- =========================
CREATE TABLE task_custom_field_values (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    option_id TEXT,
    value_text TEXT,
    value_number REAL,
    value_date TIMESTAMP,
    value_boolean BOOLEAN,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_fields(field_id),
    FOREIGN KEY (option_id) REFERENCES custom_field_options(option_id)
);
