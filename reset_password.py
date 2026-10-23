#!/usr/bin/env python3
"""
Quick Password Reset Tool for Django Admin
Usage:
    python reset_password.py <new_password>
Example:
    python reset_password.py MyPassword123!
"""

import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

try:
    import django
    django.setup()
    from django.contrib.auth.models import User

    new_pass = sys.argv[1] if len(sys.argv) > 1 else "Admin@123"

    for username in ['admin', 'divya']:
        user, created = User.objects.get_or_create(username=username)
        user.set_password(new_pass)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        status = "Created & Set" if created else "Updated"
        print(f"[{status}] Username: '{username}' | Password set to: '{new_pass}'")

    print(f"\n--> Success! You can now log into http://127.0.0.1:8000/admin/")
    print(f"    Username: divya (or admin)")
    print(f"    Password: {new_pass}")

except Exception as e:
    print(f"Error resetting password: {e}")
