import django
django.setup()

from job_app.model.users import User

try:

    instace = User.objects.create(
        username="adminsuper",
        first_name="Admin",
        last_name="User",
        email="admin@yomail.com",
        mobile="9878755878",
        is_staff=True,
        is_active=True,
    )

    instace.set_password("123456")
    instace.save()
except Exception as e:
    print("Exception : ", e)

