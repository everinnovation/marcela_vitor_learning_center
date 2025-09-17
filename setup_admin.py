#!/usr/bin/env python
import os
import sys
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

def setup_admin_user():
    """Set up an admin user for testing the admin panel."""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    # Check if the user already exists
    if User.objects.filter(username=username).exists():
        print(f"Admin user '{username}' already exists.")
        return
    
    # Create a superuser
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created admin user '{username}' with password '{password}'")
    print("You can now log in to the admin panel at /admin/ or /admin-panel/")

if __name__ == "__main__":
    setup_admin_user()
    print("Admin setup completed successfully.")
    sys.exit(0)
