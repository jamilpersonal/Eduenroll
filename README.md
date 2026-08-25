# EduEnroll — Student Course Registration System

A Django course-enrollment app with 10 pre-seeded courses, per-student
enrollment, a module/topic learning path, and AJAX "mark as complete"
progress tracking.

## Stack

- **Backend:** Django 6 (Python), SQLite
- **Frontend:** Server-rendered templates, vanilla CSS + JS (no build step)
- **Auth:** Django's built-in `User` model, one-to-one with a `Student` profile

## Project layout

```
eduenroll/
    manage.py
    seed.py                     # populates the 10 courses + demo accounts
    eduenroll/                  # project settings & root urls
        settings.py
        urls.py
    courses/                    # main app
        models.py                # Student, Course, Module, Topic, Enrollment, StudentTopicProgress
        views.py
        urls.py
        admin.py
        templates/courses/       # login.html, dashboard.html, course_detail.html, base.html
        static/css/style.css
        static/js/course_detail.js
```

## Setup

```bash
cd eduenroll
pip install django
python manage.py migrate
python seed.py          # creates the 10 courses/modules/topics + demo students
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — it redirects to the dashboard, which itself
redirects unauthenticated visitors to `/login/`.

## Demo accounts

| Username | Password       | Role    |
|----------|----------------|---------|
| student1 | eduenroll123   | Student |
| student2 | eduenroll123   | Student |
| admin    | admin12345     | Superuser (Django admin at `/admin/`) |

Re-running `python seed.py` is safe — it skips courses that already exist and
won't duplicate demo accounts.

## How it works

- **Login** (`/login/`) — username/password form against Django auth; no
  self-signup, matching the "pre-seeded database" requirement.
- **Dashboard** (`/dashboard/`) — shows "My Courses" (enrolled, with a
  progress bar) and the full 10-course catalog with an **Enroll** button.
- **Enroll** (`POST /course/<id>/enroll/`) — creates an `Enrollment` row,
  unique per (student, course).
- **Course detail / learning path** (`/course/<id>/`) — lists every Module
  in order, each with its Topics as checkboxes, plus an overall progress bar.
  Only enrolled students can view a course's path.
- **Mark topic complete** (`POST /topic/<id>/toggle/`) — a JSON AJAX endpoint
  (see `static/js/course_detail.js`) that flips completion state and returns
  the updated progress numbers, so the checkbox and progress bar update
  without a full page reload.

### A schema note

The brief's `Topic.is_completed` field is kept as specified, but topics are
shared course content — if two students enroll in the same course, a single
boolean on `Topic` would mean one student's checkbox toggles it for everyone
else too. To keep completion state correctly isolated per student, actual
"done/not done" tracking lives in a small additional model,
`StudentTopicProgress (student, topic, is_completed)`, and all progress
percentages are computed per student from that table.

## Admin panel

`/admin/` lets you add/edit courses, modules, topics, and view enrollments
and per-student progress directly (log in with the `admin` account above).

## Design

Blue/white theme built around a "learning path" motif: modules render as
numbered stops along a vertical rail on the course detail page, echoing the
sequential nature of a curriculum. Palette: navy `#0E2A4D`, blue `#2C56D6`,
teal accent `#17ADA4`, on a soft paper background `#F6F8FC`. Headings use
Sora, body text uses Inter (loaded from Google Fonts in `base.html`).
