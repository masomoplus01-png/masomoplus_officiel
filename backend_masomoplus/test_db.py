from django.db import connection

connection.ensure_connection()
with connection.cursor() as cursor:
    cursor.execute("SELECT version();")
    print(cursor.fetchone()[0])