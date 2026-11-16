# Service Request Management – Group 19

**Group:** 19  
**Group leader:** Atera David  
**Project:** Service Request Management Lab

A Django project demonstrating service-level due dates, resolution validation,
Admin filtering, automated tests, synthetic data, and query-plan inspection.

## 1. Setup

Use Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

The project defaults to SQLite so the application and tests can be explored
without a MySQL server. The assignment's MySQL acceptance criteria must be
verified against your group's MySQL database.

## 2. Configure MySQL

Create a MySQL database, for example `service_request_lab`. Set these
environment variables before running Django:

**Windows PowerShell**
```powershell
$env:DB_ENGINE="mysql"
$env:DB_NAME="service_request_lab"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

**macOS/Linux**
```bash
export DB_ENGINE=mysql
export DB_NAME=service_request_lab
export DB_USER=root
export DB_PASSWORD='your_mysql_password'
export DB_HOST=127.0.0.1
export DB_PORT=3306
```

Do not commit passwords or secret settings to GitHub.

## 3. Migration discipline

The initial schema is in `requests_app/migrations/0001_initial.py`.
The extension is in `requests_app/migrations/0002_service_request_due_at_and_resolution_summary.py`.
Do not edit `0001_initial.py`.

Inspect and apply the extension:

```bash
python manage.py showmigrations requests_app
python manage.py sqlmigrate requests_app 0002
python manage.py migrate
```

The second migration adds nullable `due_at`, blank `resolution_summary`, and
the composite index `status_due_idx` on `(status, due_at)`.

## 4. Admin

Create an administrator and start the server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/`. Service requests display due dates and
resolution summaries, support searching resolution summaries, and have an
Overdue filter.

## 5. Automated tests

```bash
python manage.py test
```

Tests use Django's test database and synthetic records only.

## 6. Synthetic data and query evidence

```bash
python manage.py seed_lab_data
python manage.py analyse_requests
```

The seed command creates at least 12 synthetic requests across two categories
and four statuses. The analysis command:
- finds requests due before a selected timestamp;
- queries OPEN or ASSIGNED requests in the IT category, ordered by priority
  and creation date;
- prints the generated SQL and `EXPLAIN` output.

Record the actual output from your MySQL environment in your submission.
MySQL may choose a table scan for a tiny table because scanning a few rows can
be cheaper than using an index. Do not claim an index was used unless the
actual MySQL `EXPLAIN` output confirms it.

## 7. GitHub submission

Create a new public or lecturer-approved private repository named
`service-request-lab`. Upload the contents of this folder (not the ZIP file
itself) to the repository. Include the repository URL in your submission.

**Submission details**
- Group: 19
- Group leader: Atera David
- Repository link: add your GitHub URL after creating the repository.

## 8. Important verification note

This source package includes the initial and extension migration files and
automated tests. The MySQL-specific migration application and query plan must
be run on the MySQL server your class uses; a local SQLite test run is not
proof of MySQL index creation or MySQL index selection.
