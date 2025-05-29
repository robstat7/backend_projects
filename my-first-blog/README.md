Project based on Django Girls Tutorial (https://tutorial.djangogirls.org/en/).

-------------

A. INSTALLATION

1. Create a virtual environment for the project and activate it
2. Run `pip install -r requirements.txt`
3. Create a `.env` file in the project root and add a secret key like `SECRET_KEY=your-very-secret-django-key-here`

    Note: Although not required, you can generate a secure secret key with:

    `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

4. Run `python manage.py migrate`.
5. Create a superuser using `python manage.py createsuperuser`.
6. Run `python manage.py runserver`
7. See `blog/urls.py` and browse urls from there to add, edit, view, and remove posts.


