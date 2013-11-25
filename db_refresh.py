#!/usr/bin/env python
import os

os.system("sudo -u postgres dropdb food-site")
os.system("sudo -u postgres createdb -O jcgrant food-site")
