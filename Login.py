import streamlit as st
import db as dbt
dbt.create_table()


    
def main():
    dbt.create_table()
    dbt.create_investment_table()
    #dbt.drop_table()
    st.title("Falcon Investors Login Page")
    st.divider()
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")
        email_id = st.text_input("Email ID")
        falcon_id = st.text_input("Falcon ID")
        password = st.text_input("Password", type='password')
        col1,col2 = st.columns(2)
        with col1:
          if st.button("Login"):
              user = dbt.authenticate_user(email_id,falcon_id ,password)
              if user:
                  st.success(f"Welcome Investor {email_id}-{falcon_id}!")
                  if user:
                    st.session_state["logged_in"] = True
                    st.session_state["email_id"] = email_id
                    st.session_state["user_id"] = user["id"]  # Store user ID
                    st.session_state["falcon_id"] = falcon_id
                    st.success("Login successful!")
                    st.switch_page("pages/investment.py")  # Redirect to investment page
              else:
                  st.error("Invalid credentials! Try again.")      
    elif choice == "Register":
        st.subheader("Create a New Account")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        new_pass = st.text_input("Password", type='password')
        falcon_id = st.text_input("Falcon ID")
        role = st.selectbox("Role", ["Investor"])
        email_id = st.text_input("Email ID")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country")
        phone = st.text_input("Phone")
        if st.button("Register"):
            if dbt.register_user(first_name,last_name, new_pass, falcon_id, role, email_id, city, state,country, phone):
                st.success("Registration successful! Please login.")
            else:
                st.error("Email ID and Falcon ID already exists! Try another one.")



if __name__ == '__main__':
  main()
  
  