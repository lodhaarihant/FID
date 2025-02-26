import streamlit as st
import qrcode
import os
import sqlite3
import db as dbt
from PIL import Image

def generate_qr(payment_url):
    qr = qrcode.make(payment_url)
    qr_path = "qr_code.png"
    qr.save(qr_path)
    return qr_path

def show_payments():
    st.subheader("Payment Records", divider='rainbow')
    
    # Get values from session state
    falcon_id = st.session_state.get("falcon_id", "")
    email = st.session_state.get("email_id", "")
    user_id = st.session_state.get("user_id", "")
    
    # Fetch data from the database
    data = dbt.fetch_all_payments(falcon_id, email, user_id)
    if not data:
        st.write("No payments recorded yet.")
        return
    
    # Create a table for better visualization
    st.table([
        {
            "User ID": row[0],
            "Name": row[1],
            "Email": row[2],
            "Phone": row[3],
            "City": row[4],
            "State": row[5],
            "Falcon ID": row[6],
            "Invested Amount (₹)": row[7],
            "Investment Date": row[8],
            "Maturity Date": row[9],
            "Attachment": row[10],
            "Payment Amount (₹)": row[11],
            "Transaction ID": row[12]
        }
        for row in data
    ])

def payment():
    # Initialize Database
    dbt.create_payment_table()
    
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("You must log in first!")
        st.stop()
    
    st.subheader("Association Details", divider='rainbow')
    
    col1, col2 = st.columns([1, 3])

    with col1:
        user_id = st.text_input("User ID", value=st.session_state.get("user_id", ""), 
                                disabled=True, key="assoc_user_id")  # Added unique key
        email = st.text_input("Email ID", value=st.session_state.get("email_id", ""), 
                            disabled=True, key="assoc_email")  # Added unique key

    with col2:
        falcon_id = st.text_input("Falcon ID", value=st.session_state.get("falcon_id", ""), 
                                disabled=True, key="assoc_falcon_id")  # Added unique key
        amount = st.selectbox("Select Amount", [0, 500, 1000, 2000], key="assoc_amount")  # Added unique key
    
    # QR Code for Payment
    if st.button("Generate QR Code", key="gen_qr_btn"):  # Added unique key
        payment_url = f"upi://pay?pa=your_upi_id@bank&pn=Association&am={amount}&cu=INR"
        qr_path = generate_qr(payment_url)
        st.image(qr_path, caption="Scan to Pay", width=200)
        
        # Generate transaction ID
        transaction_id = f"TXN{os.urandom(4).hex().upper()}"
        
        # Create a container for the Pay button to avoid nesting st.button within another st.button context
        pay_container = st.container()
        if pay_container.button("Pay", key="pay_btn"):  # Added unique key
            if dbt.insert_payment(falcon_id, amount, transaction_id):
                st.success(f"✅ Payment of ₹{amount} recorded! Your Transaction ID: {transaction_id}")
    
    with st.expander("💼 View Payments", expanded=True):  # Added unique key
        show_payments()  
  

if __name__ == "__main__":
    payment()
   