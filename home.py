import streamlit as st
import db as dbt
import time as time
import investment as inv
import association as ass

# Ensure tables exist
dbt.create_table()
dbt.create_investment_table()


    
def login():
    st.subheader("Login Section", divider="rainbow")    
    email_id = st.text_input("Email ID", key="login_email_1")  # Added unique key
    falcon_id = st.text_input("Falcon ID", key="login_falcon_1")  # Added unique key
    password = st.text_input("Password", type="password", key="login_password")  # Added unique key

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_button"):  # Added unique key
            user = dbt.authenticate_user(email_id, falcon_id, password)
            if user:
                st.success(f"Welcome Investor {email_id} - {falcon_id}!")

                # Store session values
                st.session_state["logged_in"] = True
                st.session_state["email_id"] = email_id
                st.session_state["user_id"] = user["id"]  # Store user ID
                st.session_state["falcon_id"] = falcon_id
                
                st.success("Login successful! Redirecting to investments...")

                # Change page and rerun
                st.session_state["page"] = "investment"
                st.rerun()  # Force a rerun after login
            else:
                st.error("Invalid credentials! Try again.")

def register():
    st.session_state["page"] = "register"
    st.subheader("Register a New Account", divider='rainbow')
    first_name = st.text_input("First Name", key="reg_first_name")  # Added unique key
    last_name = st.text_input("Last Name", key="reg_last_name")  # Added unique key
    new_pass = st.text_input("Password", type="password", key="reg_password")  # Added unique key
    falcon_id = st.text_input("Falcon ID", key="reg_falcon")  # Added unique key
    role = st.selectbox("Role", ["Investor"], key="reg_role")  # Added unique key
    email_id = st.text_input("Email ID", key="reg_email")  # Added unique key
    city = st.text_input("City", key="reg_city")  # Added unique key
    state = st.text_input("State", key="reg_state")  # Added unique key
    country = st.text_input("Country", key="reg_country")  # Added unique key
    phone = st.text_input("Phone", key="reg_phone")  # Added unique key

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register", key="register_submit_button"):  # Added unique key
            if dbt.register_user(first_name, last_name, new_pass, falcon_id, role, email_id, city, state, country, phone):
                st.success("Registration successful! Please login.")
                # Redirect to login after successful registration
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error("Email ID and Falcon ID already exist! Try another one.")
  

def logout():
    """Logs out the user by resetting session state and redirecting to login."""
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    
    st.success("Logged out successfully!")
    st.rerun()  # Refresh UI to show login menu

