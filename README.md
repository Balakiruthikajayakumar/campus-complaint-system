## Smart Campus System (Django + PostgreSQL)

### Setup
- **Create virtualenv** and install:

```bash
pip install -r requirements.txt
```

- **Configure environment variables**
  - Copy `.env.example` to `.env`
  - Set your PostgreSQL credentials and Gmail app password

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

