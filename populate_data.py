import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ftea.settings')

import django

django.setup()

from ftea.models import Project
from faker import Faker

fakgen = Faker()

