#!/bin/bash

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('testuser', 'test@test.com', 'test')" | python manage.py shell