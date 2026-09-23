from django.db import connection

connection.ensure_connection()
with connection.cursor() as cursor:
    if connection.vendor == "sqlite":
        cursor.execute("SELECT sqlite_version();")
    else:
        cursor.execute("SELECT version();")
    print(cursor.fetchone()[0])