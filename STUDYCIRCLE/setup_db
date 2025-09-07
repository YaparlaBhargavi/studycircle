# This script is used to set up the database and tables required by the application.
# It can be run independently to re-create the database schema.

import mysql.connector
from mysql.connector import errorcode

# --- Database Configuration ---
# Use the same credentials as your main application
DB_NAME = "circle"
DB_USER = "root"
DB_PASSWORD = "cseds@32"
DB_HOST = "localhost"

# SQL statements for creating tables and inserting initial data
TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `name` VARCHAR(100) NOT NULL,"
    "  `email` VARCHAR(100) UNIQUE NOT NULL,"
    "  `password` VARCHAR(100) NOT NULL"
    ") ENGINE=InnoDB")

TABLES['subjects'] = (
    "CREATE TABLE `subjects` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `name` VARCHAR(100) UNIQUE NOT NULL"
    ") ENGINE=InnoDB")

TABLES['progress_tracking'] = (
    "CREATE TABLE `progress_tracking` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `user_id` INT,"
    "  `subject` VARCHAR(100),"
    "  `topic_name` VARCHAR(255),"
    "  `progress_status` ENUM('Not Started', 'In Progress', 'Completed'),"
    "  `update_text` TEXT,"
    "  `study_hours` FLOAT DEFAULT 0,"
    "  `session_count` INT DEFAULT 0,"
    "  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)"
    ") ENGINE=InnoDB")

TABLES['chat'] = (
    "CREATE TABLE `chat` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `user_id` INT NOT NULL,"
    "  `subject` VARCHAR(255),"
    "  `message` TEXT NOT NULL,"
    "  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)"
    ") ENGINE=InnoDB")

TABLES['reminders'] = (
    "CREATE TABLE `reminders` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `user_id` INT NOT NULL,"
    "  `subject` VARCHAR(255) NOT NULL,"
    "  `message` TEXT NOT NULL,"
    "  `scheduled_time` DATETIME NOT NULL,"
    "  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,"
    "  `email_sent` BOOLEAN DEFAULT FALSE,"
    "  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)"
    ") ENGINE=InnoDB")

def create_database():
    try:
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cursor = cnx.cursor()
        print(f"✅ Connected to MySQL server.")
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' created or already exists.")
        
        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        print(f"❌ Failed to create database: {err}")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return False
    return True

def create_tables():
    try:
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()

        for table_name, table_sql in TABLES.items():
            try:
                print(f"Creating table {table_name}: ", end='')
                cursor.execute(table_sql)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        
        cursor.close()
        cnx.close()
        return True

    except mysql.connector.Error as err:
        print(f"❌ Failed to create tables: {err}")
        return False

def insert_subjects():
    try:
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()

        subjects = [
            'Machine Learning',
            'Software Engineering',
            'Operating System',
            'Trinkering Lab',
            'Full Stack Development'
        ]
        
        insert_sql = "INSERT IGNORE INTO subjects (name) VALUES (%s)"
        cursor.executemany(insert_sql, [(s,) for s in subjects])
        cnx.commit()
        print(f"✅ Inserted {cursor.rowcount} new subjects into the 'subjects' table.")
        
        cursor.close()
        cnx.close()
        return True

    except mysql.connector.Error as err:
        print(f"❌ Failed to insert subjects: {err}")
        return False

if __name__ == '__main__':
    if create_database():
        if create_tables():
            insert_subjects()
            print("\nDatabase setup complete!")
