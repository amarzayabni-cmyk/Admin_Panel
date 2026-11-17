import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
DATABASE_PATH = os.path.join(BASE_DIR, "data", "Register.db")
SECRET_KEY = os.environ["SECRET_KEY"]
