# import sqlite3
# import csv

# # Connect to SQLite database
# conn = sqlite3.connect("masafa.sqlite3")
# cursor = conn.cursor()

# # Get existing columns from the database
# cursor.execute("PRAGMA table_info(masafa_app_supplier);")
# existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names from PRAGMA output

# # Read CSV file
# with open("data/masafa_app_supplier.csv", "r") as file:
#     csv_reader = csv.reader(file)
    
#     # Extract column names from the first row (header)
#     csv_columns = next(csv_reader)

#     # Filter columns: Only keep those that exist in the database
#     valid_columns = [col for col in csv_columns if col in existing_columns]
    
#     if not valid_columns:
#         print("No valid columns found in CSV that match the database. Exiting...")
#         conn.close()
#         exit()

#     # Prepare SQL query with only valid columns
#     placeholders = ", ".join(["?" for _ in valid_columns])
#     query = f"INSERT INTO masafa_app_supplier ({', '.join(valid_columns)}) VALUES ({placeholders})"

#     # Insert each row into the database
#     for row in csv_reader:
#         # Map CSV row values to valid columns
#         row_data = [row[csv_columns.index(col)] for col in valid_columns]
#         try:
#             cursor.execute(query, row_data)
#         except sqlite3.Error as e:
#             print(f"Skipping row {row} due to error: {e}")

# # Commit and close connection
# conn.commit()
# conn.close()

# print("Data imported successfully (skipping missing columns).")




# import sqlite3

# def convert_numeric_fields(db_path, table_name):
#     # Connect to SQLite database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Get numeric columns (INTEGER, REAL)
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     columns = [(row[1], row[2]) for row in cursor.fetchall() if row[2] in ("INTEGER", "REAL")]

#     if not columns:
#         print(f"No numeric fields found in {table_name}. Exiting...")
#         conn.close()
#         return

#     # Fetch all rows
#     cursor.execute(f"SELECT rowid, {', '.join(col[0] for col in columns)} FROM {table_name}")
#     rows = cursor.fetchall()

#     # Process each row
#     for row in rows:
#         row_id = row[0]
#         updates = {}
#         for idx, (col_name, col_type) in enumerate(columns, start=1):
#             value = row[idx]

#             if value in (None, "", " "):  # If empty, set to 0
#                 new_value = 0
#             else:
#                 try:
#                     new_value = int(value) if col_type == "INTEGER" else float(value)
#                 except ValueError:
#                     new_value = 0  # Default to 0 if conversion fails

#             # Only update if value has changed
#             if new_value != value:
#                 updates[col_name] = new_value

#         # Apply updates if necessary
#         if updates:
#             set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
#             values = list(updates.values()) + [row_id]
#             cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?", values)

#     # Commit and close connection
#     conn.commit()
#     conn.close()
#     print(f"Numeric fields in {table_name} converted successfully.")

# # Example Usage
# convert_numeric_fields("masafa.sqlite3", "masafa_app_item")


import sqlite3

def clean_foreign_keys(db_path, table_name):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get foreign key columns
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    fk_columns = {row[3] for row in cursor.fetchall()}  # Column name is in index 3

    if not fk_columns:
        print(f"No foreign key fields found in {table_name}. Exiting...")
        conn.close()
        return

    # Fetch all rows with foreign key columns
    cursor.execute(f"SELECT rowid, {', '.join(fk_columns)} FROM {table_name}")
    rows = cursor.fetchall()

    # Process each row
    for row in rows:
        row_id = row[0]
        updates = {}

        for idx, col_name in enumerate(fk_columns, start=1):
            value = row[idx]

            if value in ("", " "):  # Convert empty string to NULL
                updates[col_name] = None

        # Apply updates if necessary
        if updates:
            set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
            values = list(updates.values()) + [row_id]
            cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?", values)

    # Commit and close connection
    conn.commit()
    conn.close()
    print(f"Foreign keys in {table_name} cleaned successfully.")

# Example Usage
clean_foreign_keys("masafa.sqlite3", "masafa_app_invoice")
