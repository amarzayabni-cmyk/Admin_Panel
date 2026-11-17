# Admin_Panel

A Python Flask application that collects a surname, first name, phone number, and email. Records are stored in the `data/Register.db` SQLite database. An authenticated admin page displays registrations and can download them as an Excel file.

## Run the app

```bash
cd "/Users/macbook/Desktop/Сургалт/web"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ADMIN_PASSWORD='choose-a-strong-password'
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
python3 app.py
```

Set both environment variables before starting the application. Do not commit credentials or secret keys to the repository.

Then open:

- Registration page: http://localhost:5000/register
- Admin login: http://localhost:5000/admin/login

## Admin access

Sign in with the password set in `ADMIN_PASSWORD`. From the admin page, view saved registrations or select **Excel татах** to download an `.xlsx` file.

## Notes

- Email validation checks for formats such as `name@example.com` and `first.last@company.com`.
- Registration submissions are saved only in SQLite; an Excel workbook is generated when the admin requests a download.
