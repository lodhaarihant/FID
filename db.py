import streamlit as st
import sqlite3 as sql
import pandas as pd

def get_db():
    conn = sql.connect('falcon.db')
    conn.row_factory = sql.Row
    return conn
  
  
def drop_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('Drop  TABLE IF  EXISTS falcon_users')
    conn.commit()
    conn.close()

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS falcon_users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT NOT NULL,
                      last_name TEXT NOT NULL,
                      password TEXT NOT NULL,
                      falcon_id TEXT UNIQUE NOT NULL,
                      role TEXT DEFAULT 'Investor',
                      email_id TEXT UNIQUE NOT NULL,
                      city TEXT NOT NULL,
                      state TEXT NOT NULL,
                      country TEXT NOT NULL,
                      phone TEXT NOT NULL
                  )''')
    conn.commit()
    conn.close()

def register_user(first_name,last_name, password, falcon_id, role, email_id, city, state,country, phone):
    conn = get_db()
    try:
        conn.execute("INSERT INTO falcon_users (first_name,last_name, password, falcon_id, role, email_id, city, state, country, phone) VALUES (?, ?, ? ,?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, password, falcon_id, role, email_id, city, state ,country, phone))
        conn.commit()
        return True
    except sql.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email_id, falcon_id, password):
    conn = get_db()
    user = conn.execute("SELECT * FROM falcon_users WHERE  email_id = ? and falcon_id = ?  and password = ? ", ( email_id, falcon_id, password)).fetchone()
    conn.close()
    return user
  
  
  
def create_investment_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS falcon_investment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            falcon_id TEXT NOT NULL,
            invested_amount TEXT NOT NULL,
            investment_date TEXT NOT NULL,
            maturity_date TEXT NOT NULL,
            attachment TEXT,
            FOREIGN KEY (user_id) REFERENCES falcon_users(id)
        )
    ''')
    conn.commit()
    conn.close()
  

def insert_investment(user_id, falcon_id, amount, invest_date, maturity_date, attachment):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO falcon_investment (user_id, falcon_id, invested_amount, investment_date, maturity_date, attachment) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id, falcon_id, amount, invest_date, maturity_date, attachment)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False
    
    
def fetch_all_investments():
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT fi.invested_amount, 
                   fi.investment_date, fi.maturity_date, fi.attachment
            FROM falcon_investment fi
            JOIN falcon_users fu ON fi.user_id = fu.id
            ORDER BY fi.investment_date DESC
        ''')
        investments = cursor.fetchall()  # Fetch all investment records
        df = pd.DataFrame(investments, columns=["Invested Amount", "Investment Date", "Maturity Date", "Attachment"])
        # Convert file paths to clickable links
        
    # Convert to float and properly format numbers without scientific notation
        df["Invested Amount"] = df["Invested Amount"].astype(float).map('{:,.2f}'.format)
    
        df["Attachment"] = df["Attachment"].apply(lambda x: f'<a href="{x}" target="_blank">View File</a>' if x else "No Attachment")
        return df

    except sql.Error as e:
        print("Error fetching investments:", e)
        return []

    finally:
        conn.close()