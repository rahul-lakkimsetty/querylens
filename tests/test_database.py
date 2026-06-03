import unittest
import sqlite3
import os
import tempfile
from flask import Flask
from app.database import get_schema_info, execute_select_query, get_db_connection

class DatabaseTestCase(unittest.TestCase):
    """
    Test suite for app/database.py functionality.
    Verifies SQLite connections, schema extraction, and query execution.
    """
    def setUp(self):
        # Create a temporary file to act as our test SQLite database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Configure a test Flask app
        self.app = Flask(__name__)
        self.app.config["DATABASE_PATH"] = self.db_path
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Seed the test database with sample structure
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE test_customers (
                customer_id TEXT PRIMARY KEY,
                customer_zip_code_prefix INTEGER NOT NULL,
                customer_city TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE test_orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_status TEXT,
                order_purchase_timestamp TEXT
            );
        """)
        cursor.execute("INSERT INTO test_customers VALUES ('cust1', 1001, 'Sao Paulo');")
        cursor.execute("INSERT INTO test_customers VALUES ('cust2', 2002, 'Rio de Janeiro');")
        conn.commit()
        conn.close()

    def tearDown(self):
        # Pop the context and remove the temporary file
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_schema_retrieval(self):
        """Verify that get_schema_info correctly extracts tables, columns, and types."""
        schema = get_schema_info()
        
        # Verify both tables exist in catalog
        self.assertIn("test_customers", schema)
        self.assertIn("test_orders", schema)
        
        # Verify columns of test_customers table
        cust_cols = schema["test_customers"]
        self.assertEqual(len(cust_cols), 3)
        
        cust_col_names = {col["name"]: col for col in cust_cols}
        self.assertIn("customer_id", cust_col_names)
        self.assertEqual(cust_col_names["customer_id"]["type"], "TEXT")
        self.assertTrue(cust_col_names["customer_id"]["primary_key"])
        
        self.assertIn("customer_zip_code_prefix", cust_col_names)
        self.assertEqual(cust_col_names["customer_zip_code_prefix"]["type"], "INTEGER")
        self.assertFalse(cust_col_names["customer_zip_code_prefix"]["primary_key"])

    def test_execute_select_query_success(self):
        """Verify executing a valid SELECT query fetches rows as a dict list."""
        results = execute_select_query("SELECT customer_id, customer_city FROM test_customers ORDER BY customer_id;")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["customer_id"], "cust1")
        self.assertEqual(results[0]["customer_city"], "Sao Paulo")
        self.assertEqual(results[1]["customer_id"], "cust2")
        self.assertEqual(results[1]["customer_city"], "Rio de Janeiro")

    def test_execute_select_query_failure(self):
        """Verify that invalid SQL queries throw an operational database error."""
        with self.assertRaises(sqlite3.OperationalError):
            # Querying a non-existent table
            execute_select_query("SELECT * FROM non_existent_table;")

if __name__ == "__main__":
    unittest.main()
