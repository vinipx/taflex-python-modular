# Database Operations

The `database_manager` utility provides a unified way to interact with PostgreSQL and MySQL databases using **SQLAlchemy**.

## Configuration

Ensure you have your database credentials and connection strings ready. TAFLEX PY supports secure, parameterized queries to prevent SQL injection.

## Usage

```python
from src.core.utils.database_manager import database_manager

# 1. Connect to PostgreSQL
# Format: postgresql+psycopg2://user:password@host:port/dbname
database_manager.connect_postgres(
    connection_id='my_pg_db', 
    connection_string='postgresql+psycopg2://admin:secret@localhost:5432/test_db'
)

# 2. Execute a Query
# Returns a list of dictionaries (rows)
users = database_manager.query(
    'my_pg_db', 
    'SELECT * FROM users WHERE status = :status', 
    parameters={'status': 'active'}
)

print(f"Found {len(users)} active users.")
if users:
    print(f"First user: {users[0]['username']}")

# 3. Connect to MySQL
# Format: mysql+pymysql://user:password@host:port/dbname
database_manager.connect_mysql(
    connection_id='my_mysql_db',
    connection_string='mysql+pymysql://root:pass@localhost:3306/inventory'
)

# 4. Insert / Update Data
database_manager.query(
    'my_mysql_db',
    'INSERT INTO logs (message) VALUES (:msg)',
    parameters={'message': 'Test started'}
)

# 5. Close connections
database_manager.close() # Closes all sessions
```

## Best Practices

- **Connection IDs**: Use meaningful IDs for your connections to manage multiple databases simultaneously.
- **Cleanup**: Always call `database_manager.close()` in your `conftest.py` teardown or at the end of your test suite to release pooled connections.
- **SQL Injection**: Never use f-strings to build your queries. Always use the `:variable` syntax and pass the `parameters` dictionary to the `query()` method.
