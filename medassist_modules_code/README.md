# MedAssist AI – Module 1 and Module 2 (Django + SQLite)

This is a standalone Django implementation of:
- Module 1: Patient Profile Management
- Module 2: Symptom Correlation Analysis and Medical History Integration

It uses Django's built-in authentication (`request.user`). It does not implement registration/login because your teammate is handling that. It is designed to be integrated into the same Django project later.

## 1. Setup

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
django-admin startproject medassist .
py manage.py startapp profiles
py manage.py startapp symptoms
```

Copy the supplied `medassist/settings_additions.py` contents into your generated `medassist/settings.py`:
- Add `profiles` and `symptoms` to `INSTALLED_APPS`.
- Keep Django's default SQLite database.
- Add the `TEMPLATES` DIRS setting shown in the file.
- Add `LOGIN_URL = "login"` if your teammate's login URL is named `login`; otherwise change it to their URL name.

Copy the supplied files into the matching locations. Keep the generated `manage.py`, `medassist/asgi.py`, `medassist/wsgi.py`, and `medassist/__init__.py`.

## 2. Database and sample data

```bash
py manage.py makemigrations profiles symptoms
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Log in using a user account. For a quick local test, create a user in Django admin or use your teammate's login.

Load the illustrative sample dataset:

```bash
py manage.py load_symptom_dataset
```

The sample dataset is synthetic and only demonstrates code flow. It is NOT a clinically validated dataset and must not be used for diagnosis.

## 3. URLs

Include both app URL sets in `medassist/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # standalone testing only
    path("profile/", include("profiles.urls")),
    path("symptoms/", include("symptoms.urls")),
]
```

For standalone testing, include Django's built-in authentication URLs as shown. A basic login template is included in `templates/registration/login.html`. When integrating into your teammate's project, remove the `/accounts/` line if they already provide their own login URLs, and set `LOGIN_URL` to their actual login route name. Do not replace their authentication URLs.

## 4. Connect to teammate's login

Both apps use `@login_required` and the authenticated `request.user`. They do not create another login system.

If your teammate uses Django's default User model, this works directly. If they use a custom user model, Django's `request.user` still works, but check whether their custom model supports the normal authentication backend. The profile model's OneToOne relation uses `settings.AUTH_USER_MODEL`, so it supports custom user models too.

## 5. Pages

- `/profile/` – view profile
- `/profile/edit/` – create/update profile
- `/symptoms/` – choose symptoms
- `/symptoms/history/` – list your own submitted assessments
- `/symptoms/assessment/<id>/` – view one of your own assessments

## 6. Add medical history

Medical history is entered by the signed-in patient in this student prototype. It is private to that user. Do not enter real patient data during demonstrations.

## 7. Dataset format

The loader accepts a CSV with columns:
- `disease`
- one column per symptom, with values such as `1`, `0`, `yes`, `no`, `true`, `false`

Default file: `symptoms/data/sample_symptom_dataset.csv`.

To load another CSV:
```bash
py manage.py load_symptom_dataset --file "C:/path/to/dataset.csv"
```

The correlation component reports:
- how many dataset rows contain each selected symptom
- pairwise co-occurrence counts and Jaccard similarity
- dataset rows matching all selected symptoms

These are dataset associations only. Correlation does not establish causation or diagnose disease. Disease labels are not used to generate a prediction.

## 8. Integration note

If the team already has profile or medical-history models, do not create duplicate tables. Merge the fields and relationships with the team's existing models after coordinating with the team. Run migrations only after reviewing the shared project.
