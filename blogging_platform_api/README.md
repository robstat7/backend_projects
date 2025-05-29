### Blogging Platform API Project

------------

A. INSTALLATION

1. Create a virtual environment for the project and activate it.

2. Run `pip install -r requirements.txt`.

3. Create a `.env` file in the project root and add a secret key like `SECRET_KEY=your-very-secret-django-key-here`

    Note: Although not required, you can generate a secure secret key with:

    `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

4. Run `python manage.py migrate`.

5. Run `python manage.py shell` and inside the shell, do:
    `>>> from blog.models import Category`
    `>>> Category.objects.create(name="productivity")`
    `>>> Category.objects.create(name="spirituality")`
    `>>> ^D`

    This will create our two categories into the database.

6. Run `python manage.py runserver`

7. You can now do CRUD operations on posts.


B. Example POST Requests to /posts:

1.
{
"title": "Hello World",
"content": "Raam Raam ji. This is my first blog post!",
"categories": ["productivity"]
}

2.
{
"title": "Hello World 2",
"content": "Raam Raam ji. This is my second blog post!",
"categories": ["productivity", "spirituality"]
}