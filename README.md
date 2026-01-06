## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone <repository-url>
cd your_filename

pip install -r requirements.txt
python src/main.py

After successful execution, a SQLite database will be created at:
output/asana_simulation.sqlite




# Asana-Style Seed Data Generation for RL Environments

This repository contains a reproducible pipeline for generating a realistic, enterprise-scale dataset simulating an Asana-like workspace.  
The generated data is intended for use in reinforcement learning (RL) environments involving computer-use agents.

The focus of this project is **data realism, logical consistency, and clear methodology**, rather than live scraping or external API usage.

---

## 📌 Project Overview

The pipeline generates a complete relational dataset for a B2B SaaS organization, including:

- Organizations
- Users
- Teams
- Projects
- Sections
- Tasks and Subtasks
- Comments and Followers
- Custom Fields and Values

The data is designed to:
- Follow realistic enterprise usage patterns
- Maintain temporal and relational consistency
- Be deterministic and reproducible for evaluation

---

## 🧠 Data Generation Strategy

Each column in the dataset is generated using one of the following strategies:

- **LLM-inspired Heuristics**  
  Template-based natural language generation inspired by public GitHub issues and Asana templates.

- **Synthetic + Heuristics**  
  Programmatic generation using realistic distributions and constraints.

- **Derived**  
  Values deterministically derived from related entities or timestamps.

Live scraping and LLM API calls are intentionally avoided to ensure reproducibility and ease of evaluation.

---

## 📂 Repository Structure

Intern_assignment/
├── schema.sql # Database schema (DDL)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── src/
│ ├── main.py # Entry point for data generation
│ │
│ ├── generators/ # Entity-wise data generators
│ │ ├── organizations.py
│ │ ├── users.py
│ │ ├── teams.py
│ │ ├── projects.py
│ │ ├── sections.py
│ │ ├── tasks.py
│ │ ├── comments.py
│ │ ├── task_followers.py
│ │ ├── custom_fields.py
│ │ └── custom_field_values.py
│ │
│ └── utils/ # Shared utilities
│ ├── db.py # Database setup and schema execution
│ ├── faker_utils.py # Synthetic name/text helpers
│ ├── time_utils.py # Timestamp generation utilities
│ ├── logger.py # Logging configuration
│ └── validation.py # Post-generation data checks
│
└── output/
└── asana_simulation.sqlite # Generated SQLite database
