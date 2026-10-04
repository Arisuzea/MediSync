# MediSync

MediSync is a clinic system proposal for NU Dasmarinas. Students book an appointment with a doctor or dentist, answer a short triage questionnaire, receive a queue number, and follow their position in line. Clinic staff manage practitioners, schedules and the queue through the Django admin.

The project is a Django application built from a working single-file HTML prototype (`medisync-prototype.html`). The prototype remains the reference for how every student screen looks and reads. The migration replaces its in-memory demo data with real models, views, forms, sessions and database queries while keeping its content, layout and wording.

## Contents

1. [Project status](#project-status)
2. [Technology](#technology)
3. [Getting started](#getting-started)
4. [Configuration](#configuration)
5. [Demo data and accounts](#demo-data-and-accounts)
6. [Project structure](#project-structure)
7. [Architecture](#architecture)
8. [Frontend conventions](#frontend-conventions)
9. [Testing](#testing)
10. [Development workflow](#development-workflow)
11. [Sharing a local demo](#sharing-a-local-demo)
12. [Troubleshooting](#troubleshooting)
13. [Roadmap](#roadmap)

## Project status

| Stage | Scope | Status |
|-------|-------|--------|
| 0 | Project skeleton, split settings, custom User | Complete |
| 1 | Layout shell, shared templates, icons, CSS and JS structure | Complete |
| 2 | Accounts: login, logout, profile, settings, password change, data export | Complete |
| 3 | Clinic models, admin, seed data, slot generator | Next |
| 4 | Booking steps 1 to 3 (type and reason, practitioner, schedule) | Not started |
| 5 | Symptom questionnaire and triage scoring | Not started |
| 6 | Appointment confirmation, atomic booking, notifications | Not started |
| 7 | Live queue, polling, cancellation, staff call-next | Not started |
| 8 | History, dashboard, notifications, help and FAQ | Not started |
| 9 | Error pages, security review, full test sweep, production settings | Not started |

Some pages currently show sample data from `apps/core/mock.py` so that every navigation item opens. This applies to the dashboard, queue status, visit history, help, and the booking placeholders. Each stage replaces its own pages with real data. Do not build new features on top of the placeholder views or on `mock.py`. Both are deleted by the end of Stage 8.

## Technology

| Area | Choice |
|------|--------|
| Language | Python 3.11 or newer |
| Framework | Django 5.2 (`>=5.2,<5.3`) |
| Configuration | django-environ |
| Database | SQLite for development. Any database supported by `DATABASE_URL` for production. |
| Frontend | Django templates, plain CSS, vanilla JavaScript (ES modules) |
| Timezone | `Asia/Manila` |

The following are intentionally not used: Django REST Framework, Celery, Channels, Tailwind, HTMX, or any JavaScript framework. Adding any of them requires a team decision first.

## Getting started

### Prerequisites

- Python 3.11 or newer
- Git

### Setup

Clone the repository and open a terminal in the project root.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements/dev.txt
Copy-Item example.env .env
```

If PowerShell blocks the activation script, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**macOS and Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
cp example.env .env
```

Open `.env` and replace the placeholder `SECRET_KEY` with a new value. One way to generate it:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

Create the database, load the demo data, and start the server:

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

The application is available at `http://127.0.0.1:8000/` and the staff interface at `http://127.0.0.1:8000/admin/`.

Every new terminal session needs the virtual environment activated before running any `manage.py` command. A prompt that starts with `(.venv)` confirms it is active.

## Configuration

Settings are split by environment:

| File | Purpose |
|------|---------|
| `config/settings/base.py` | Shared settings. Reads environment variables. |
| `config/settings/dev.py` | Local development. Debug on, console email backend. This is the default. |
| `config/settings/prod.py` | Production. Hardening is part of Stage 9. |

`manage.py`, `wsgi.py` and `asgi.py` default to `config.settings.dev`. Select another module with the `DJANGO_SETTINGS_MODULE` environment variable or the `--settings` option.

Environment variables are read from `.env` in the project root:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | none | Django secret key. Use a unique value per environment. |
| `DEBUG` | No | `False` | Enables debug mode. Settings in `dev.py` set this to `True`. |
| `ALLOWED_HOSTS` | No | empty list | Comma-separated host names. |
| `DATABASE_URL` | No | SQLite file in the project root | Database connection string, for example `postgres://user:password@localhost:5432/medisync`. |

The `.env` file, `db.sqlite3` and any file containing credentials are excluded by `.gitignore`. Never commit them. `example.env` must contain placeholder values only.

## Demo data and accounts

`python manage.py seed_demo` creates or refreshes the demo student from the prototype. The command is safe to run more than once and does not overwrite an existing password.

| Account | Username | Password | Use |
|---------|----------|----------|-----|
| Demo student | `alex.mendoza` | `medisync-demo` | Student pages |
| Superuser | the one you create with `createsuperuser` | your choice | `/admin/` |

Do not run `seed_demo` on a public server. It creates an account with a published password. Student accounts are created through the admin, because there is no public signup.

Later stages extend `seed_demo` with practitioners, visit reasons, symptoms, FAQs and sample appointments.

## Project structure

```text
medisync/
|-- manage.py
|-- example.env                 Template for .env (placeholders only)
|-- requirements/
|   |-- base.txt                Django, django-environ
|   |-- dev.txt                 Development extras (includes base)
|   `-- prod.txt                Production extras (includes base, gunicorn)
|-- config/
|   |-- settings/               base.py, dev.py, prod.py
|   |-- urls.py                 Root URL configuration
|   |-- wsgi.py
|   `-- asgi.py
|-- apps/
|   |-- core/                   Layout context, dashboard, help, icons, template tags, seed command
|   |-- accounts/               User, StudentProfile, UserSettings, authentication views
|   |-- clinic/                 Practitioners, visit reasons, symptoms, availability (Stage 3)
|   |-- appointments/           Booking flow, Appointment, triage, queue, history (Stages 4 to 8)
|   `-- notifications/          Notification model and delivery service (Stages 6 and 8)
|-- templates/
|   |-- base.html               Page shell (sidebar, top bar, content block)
|   |-- base_auth.html          Shell without navigation, used by the login page
|   |-- partials/               sidebar, topbar, toasts, signout_modal
|   |-- components/             button, badge, empty_state, form_field, modal, toggle
|   `-- <app>/                  Page templates grouped by app
|-- static/
|   |-- css/                    tokens, base, layout, components, forms, tables, feedback, responsive
|   |   `-- pages/              One stylesheet per page (auth, dashboard, queue, settings, help, booking)
|   `-- js/
|       |-- main.js             Entry point, loaded on every page
|       `-- ui/                 sidebar, dropdown, toast, modal
`-- docs/                       Project documentation
```

## Architecture

### Application responsibilities

The rule that keeps the apps separate: **clinic describes what exists, appointments describes what a student does with it.**

| App | Owns | Does not own |
|-----|------|--------------|
| `core` | Layout, dashboard, help and FAQ, error pages, template tags, icons, toast helper | Clinic or appointment data |
| `accounts` | Custom User, StudentProfile, UserSettings, login, logout, password change, data export | Appointments |
| `clinic` | Practitioner, PractitionerAvailability, VisitReason, Symptom, ClosedDate, slot generation | What a student has booked |
| `appointments` | Booking flow, Appointment, TriageAssessment, triage scoring, queue state, history, cancellation | The list of practitioners and reasons |
| `notifications` | Notification model, dropdown, SMS and email service abstraction | Deciding when to notify (the calling app does that) |

Do not create additional apps for queue or triage logic.

### Data model

```text
User
 |-- 1:1 StudentProfile
 |-- 1:1 UserSettings
 |-- 1:N Notification
 `-- 1:N Appointment
          |-- N:1 Practitioner
          |-- N:1 VisitReason
          `-- 1:1 TriageAssessment
                    `-- N:M Symptom

Practitioner
 `-- 1:N PractitionerAvailability

ClosedDate
FAQ
```

Implemented today: `User`, `StudentProfile`, `UserSettings`. The remaining models arrive in Stages 3 to 8.

Design decisions that apply across the project:

- `User` is a custom `AbstractUser`, set as `AUTH_USER_MODEL` before the first migration. Name and email live on `User`. Medical and identification data live on `StudentProfile`.
- Every user receives a `StudentProfile` and a `UserSettings` row automatically through a `post_save` signal, so views never need to handle a missing row.
- `Appointment` is the central model. Visit history is a query on `Appointment`. It is never stored separately.
- Appointment statuses: `confirmed`, `called`, `checked_in`, `completed`, `cancelled`, `no_show`. Priorities: `low`, `medium`, `high`.
- Double booking is prevented by the database with a conditional `UniqueConstraint` on practitioner, date and start time, applied only where the appointment is not cancelled. A cancelled slot can be booked again.
- Triage weights belong on `VisitReason`. Red-flag information belongs on `Symptom`. The scoring algorithm is a pure function so it can be tested without a database.
- A booking in progress is held in the Django session (type, reason, practitioner, date and slot, answers). An `Appointment` is created only after confirmation, inside a single transaction.
- Queue state (position, students ahead, estimated wait) is calculated from `Appointment` rows. It is not stored a second time.

### URL map

| URL | Page | Stage |
|-----|------|-------|
| `/` | Dashboard | 1, 8 |
| `/accounts/login/`, `/accounts/logout/` | Sign in and sign out (logout is POST only) | 2 |
| `/accounts/password/` | Change password | 2 |
| `/profile/`, `/profile/emergency/` | Medical profile and emergency contact | 2 |
| `/settings/`, `/settings/toggle/` | Settings and switches | 2 |
| `/export/` | Download personal data as JSON | 2, 8 |
| `/book/` | Booking start: visit type and reason | 4 |
| `/book/practitioner/` | Choose a practitioner | 4 |
| `/book/schedule/` | Choose a date and time slot | 4 |
| `/book/symptoms/` | Triage questionnaire | 5 |
| `/book/result/` | Triage result and estimated wait | 5 |
| `/book/confirm/` | Confirm booking (POST creates the appointment) | 6 |
| `/appointments/<ref>/` | Appointment confirmation | 6 |
| `/appointments/<ref>/cancel/` | Cancel an appointment (POST) | 7 |
| `/queue/`, `/queue/status/` | Queue page and JSON polling endpoint | 7 |
| `/history/` | Visit history | 8 |
| `/help/` | Help and FAQ | 8 |
| `/admin/` | Staff interface | all |

Pages that already exist in placeholder form use the same URLs, except confirmation, which currently lives at `/appointments/confirmation/` until Stage 6 introduces the reference-based URL.

### Access control

- All student views require authentication.
- Every appointment lookup is filtered by `request.user`. A reference that belongs to another student returns 404.
- State-changing actions (logout, cancel, confirm, settings toggles) accept POST only and are protected by CSRF.
- Staff work in the Django admin. There is no custom staff dashboard. Calling the next patient will be an admin action added in Stage 7.

## Frontend conventions

The prototype used one global state object and a single render function. The Django version replaces both with server-rendered templates and small, independent scripts.

### Templates

- Extend `base.html` and fill `{% block content %}`. Use `base_auth.html` only for pages shown before sign-in.
- Page-specific stylesheets go in `{% block extra_css %}`.
- Reuse the components in `templates/components/` rather than writing new markup for buttons, badges, form fields and modals.

Component usage:

```django
{% include "components/button.html" with label="Save changes" type="submit" variant="gold" icon="check" %}
{% include "components/badge.html" with tone="high" icon="alert" text="Allergy on file" %}
{% include "components/form_field.html" with field=form.course %}
{% include "components/toggle.html" with name="sms_alerts" on=s.sms_alerts label="SMS alerts" %}

{% load ui %}
{% modal id="signout" icon="logout" title="Sign out of MediSync?" tone="navy" %}
  ...modal body, including its own form or buttons...
{% endmodal %}
```

Open a modal with any element that has `data-modal-open="<id>"`. Close it with `data-modal-close`, a click on the backdrop, or the Escape key.

### Icons

Icons come from the template tag, using the SVG data carried over from the prototype in `apps/core/icons.py`:

```django
{% load ui %}
{% icon "bell" 18 %}
```

An unknown icon name falls back to the info icon. Add new icons to `icons.py`.

### Messages and toasts

The prototype's toast system is replaced by Django messages. Use the helper so the title and body format is kept:

```python
from apps.core.messaging import toast

toast(request, "success", "Profile saved", "Your clinic record is up to date.")
```

Accepted kinds are `success`, `info`, `warning` and `error`.

### CSS and JavaScript

- Stylesheets are split by concern. Shared tokens (colors, spacing) live in `tokens.css`. Page styles live in `static/css/pages/`.
- Use the button naming scheme `btn btn--primary`, `btn--outline`, `btn--gold`, `btn--danger`. The prototype's inconsistent class names were normalized.
- JavaScript is limited to interface behavior: sidebar toggle, dropdowns, modals, toast dismissal, questionnaire live feedback, and queue polling. Business rules belong on the server.
- Scripts are ES modules. `static/js/main.js` initializes the shared modules on every page. Page-specific scripts load from their own templates.

## Testing

Run the full suite:

```bash
python manage.py test apps
```

Run one app or one test class:

```bash
python manage.py test apps.accounts
python manage.py test apps.accounts.tests.ProfileTests
```

Before opening a pull request or marking a stage complete, run all three:

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test apps
```

The accounts suite currently covers signals and defaults, login and logout, profile validation, unique student IDs, isolation between students, settings toggles, data export, and the layout shell. Later stages must add tests for triage scoring, slot generation, double booking and permissions.

## Development workflow

Work follows the numbered stages in the roadmap. Each stage is built and tested independently before the next one starts.

Rules for every change:

1. Keep the prototype's content, wording, layout and styling. A button that only showed a toast in the prototype becomes a real feature. It is not removed.
2. Validate important input on the server and enforce integrity with database constraints.
3. Keep JavaScript small. Do not move business logic into the browser.
4. Commit migration files together with the model change that created them.
5. Do not edit working code in another app without telling its owner. Respect the app boundaries described above.
6. Anything that needs a secret reads it from the environment. Nothing sensitive is committed.

A stage is complete when:

- `manage.py check` reports no issues.
- `makemigrations --check` reports no missing migrations.
- All tests pass, including new tests for the stage.
- The new pages work at desktop and phone widths and match the prototype.
- Nothing for that stage still reads from `apps/core/mock.py`.

Known prototype defects and where they are resolved:

| Defect | Resolution | Stage |
|--------|------------|-------|
| Button class names did not match the CSS (`btn-bp` against `.bp`) | Single `btn btn--*` naming scheme | 1 (complete) |
| `.cnt` used for two unrelated purposes | Split into separate classes | 1 (complete) |
| Missing `calendarPlus` icon fell back to the wrong icon | Use the existing `calplus` icon | 1 (complete) |
| `cancelprio` could cancel the previous confirmed appointment instead of discarding the draft | Discard clears session data only. Cancel acts only on an appointment found by reference and owner. | 4 and 7 |
| 404 item in the navigation was demo scaffolding | Removed. Real error pages are added instead. | 8 and 9 |
| Automatic queue call after 8 seconds was demo scaffolding | Removed. Staff call the next patient from the admin. | 7 |

## Sharing a local demo

To show the running application to people outside your network, use a temporary tunnel. This is for demonstrations only. Do not use it for real student data.

Create `config/settings/tunnel.py` (keep it out of version control if it contains anything specific to your machine):

```python
from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".trycloudflare.com"]
CSRF_TRUSTED_ORIGINS = ["https://*.trycloudflare.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

Run the server in one terminal with the virtual environment active:

```bash
python manage.py runserver 8000 --insecure --settings=config.settings.tunnel
```

Run the tunnel in a second terminal:

```bash
cloudflared tunnel --url http://localhost:8000
```

`cloudflared` prints a public `https://*.trycloudflare.com` address. The address changes every time the tunnel restarts. The `--insecure` flag makes the development server deliver static files while `DEBUG` is off. Change the demo password with `python manage.py changepassword alex.mendoza` before sharing the link widely.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `ModuleNotFoundError: No module named 'django'` | The virtual environment is not active. Activate it, then retry. |
| `DisallowedHost` error | The host name is not in `ALLOWED_HOSTS`. Check which settings module the server reported at startup. |
| `no such table` error | Migrations have not been applied. Run `python manage.py migrate`. |
| CSRF failure on login behind a tunnel | Add the tunnel origin to `CSRF_TRUSTED_ORIGINS` and restart the server. |
| Pages load without styling | With `DEBUG` off, `runserver` needs the `--insecure` flag. |
| Server still uses old settings | The `DJANGO_SETTINGS_MODULE` variable was set in a different terminal. Use the `--settings` option instead. |
| `pip install` fails on a requirements file | Each line in `requirements/*.txt` must be a package name or an `-r` include. Remove any stray text. |

## Roadmap

Detailed goals, deliverables, acceptance criteria and test requirements for each stage are in the stage guide (`MediSync-Stage-Guide.pdf`). In summary:

- **Stage 3:** clinic models, admin registration, seed data and the slot generator.
- **Stage 4:** the first three booking steps, held in the session.
- **Stage 5:** the questionnaire and the triage scoring service.
- **Stage 6:** atomic appointment creation, confirmation page, notifications and calendar export.
- **Stage 7:** live queue with 10-second polling, cancellation, rescheduling, and staff call-next from the admin.
- **Stage 8:** history, a data-driven dashboard, notifications, FAQ management and removal of all sample data.
- **Stage 9:** error pages, security review, full tests and production configuration.

Out of scope for now: a custom staff dashboard, public signup, a real slot reservation lock (the slot hold is display only), a live SMS provider (output goes to the console in development), WebSockets, and any additional frontend or backend framework.
