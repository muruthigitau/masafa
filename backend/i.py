import sqlite3
import csv
import os

def export_database_to_csv(db_path, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        export_table(cursor, table, output_dir)
    
    conn.close()
    print(f"All tables exported to {output_dir}")

def export_table(cursor, table_name, output_dir):
    # Get column information
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Fetch all data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Write to CSV
    csv_filename = os.path.join(output_dir, f"{table_name}.csv")
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write headers
        writer.writerows(rows)  # Write data
    
    print(f"Exported {table_name} to {csv_filename}")

def import_csv_to_database(db_path, input_dir):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            table_name = os.path.splitext(filename)[0]
            csv_path = os.path.join(input_dir, filename)
            
            # Get existing columns from the database
            cursor.execute(f"PRAGMA table_info({table_name});")
            existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names
            
            with open(csv_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                csv_columns = next(csv_reader)  # Extract column names from CSV
                valid_columns = [col for col in csv_columns if col in existing_columns]
                
                if not valid_columns:
                    print(f"No valid columns found for {table_name}. Skipping...")
                    continue
                
                placeholders = ", ".join(["?" for _ in valid_columns])
                query = f"INSERT INTO {table_name} ({', '.join(valid_columns)}) VALUES ({placeholders})"
                
                # Check for existing IDs
                id_column = "id" if "id" in valid_columns else None
                
                for row in csv_reader:
                    row_data = [None if row[csv_columns.index(col)] in ("", " ") else row[csv_columns.index(col)] for col in valid_columns]
                    
                    if id_column:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?", (row_data[valid_columns.index(id_column)],))
                        if cursor.fetchone()[0] > 0:
                            print(f"Skipping row with existing ID {row_data[valid_columns.index(id_column)]}")
                            continue
                    
                    try:
                        cursor.execute(query, row_data)
                    except sqlite3.Error as e:
                        print(f"Skipping row {row} due to error: {e}")
    
    conn.commit()
    conn.close()
    print("All valid CSV data imported successfully.")

# Example Usage
# export_database_to_csv("masafa.sqlite3", "exported_tables")
import_csv_to_database("masafa.sqlite3", "exported_tables")
