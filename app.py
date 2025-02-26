import streamlit as st
import db as dbt
import home as hm
import investment as inv
import association as ass

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Ensure tables exist
dbt.create_table()
dbt.create_investment_table()

def main():
    st.title("Falcon Investors Login Page")
    st.divider()
    
    # Sidebar menu based on login state
    if st.session_state["logged_in"]:
        menu = ["Investment","Association","Logout"]
    else:
        menu = ["Login", "Register"]
    
    choice = st.sidebar.selectbox("Menu", menu)

    # Handle menu selection
    if choice == "Login":
        st.session_state['page'] = "login"
    elif choice == "Register":
        st.session_state['page'] = "register"
    elif choice == "Investment":
        st.session_state['page'] = "investment"
    elif choice == "Association":
        st.session_state['page'] = "association"
    elif choice == "Logout":
       st.session_state['page'] = "logout"
    
    # Render the appropriate page
    if st.session_state["page"] == "login":
        hm.login()
    elif st.session_state["page"] == "register":
        hm.register()
    elif st.session_state["page"] == "logout":
        hm.logout()
    elif st.session_state["page"] == "investment":
        inv.investment()
    elif st.session_state["page"] == "association":
        ass.payment()
    
    
if __name__ == "__main__":
    main()

