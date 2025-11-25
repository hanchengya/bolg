#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User

try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print("Password reset successful!")
    print("Username: admin")
    print("Password: admin123")
except User.DoesNotExist:
    print("Admin user does not exist, creating...")
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin created successfully!")
    print("Username: admin")
    print("Password: admin123")
