import streamlit as st
import db as dbt
import pandas as pd
import datetime
import os


def show_investments():
    st.subheader("Investment Details")
    investments_df = dbt.fetch_all_investments()
    if investments_df.empty:
        st.warning("No investments found.")
    else:
        # Use st.markdown with unsafe_allow_html to render HTML links
        st.markdown(investments_df.to_html(escape=False, index=False), unsafe_allow_html=True)
             
             
def investment():
    dbt.create_investment_table()
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("You must log in first!")
        st.stop()

    st.subheader("Investment Details")

    invested_amount = st.number_input("Invested Amount")
    investment_date = st.date_input("Investment Date", datetime.date.today())
    maturity_date = st.date_input("Maturity Date")
    attachment = st.file_uploader("Upload Proof (Optional)", type=["pdf", "jpg", "png"])

    if st.button("Submit Investment"):
        attachment_path = None
        if attachment:
            folder = "uploads/"
            os.makedirs(folder, exist_ok=True)
            attachment_path = os.path.join(folder, attachment.name)
            with open(attachment_path, "wb") as f:
                f.write(attachment.getbuffer())

        success = dbt.insert_investment(
            st.session_state["user_id"],
            st.session_state["falcon_id"],
            invested_amount,
            investment_date,
            maturity_date,
            attachment_path
        )

        if success:
            st.success("Investment added successfully!")
        else:
            st.error("Error saving investment. Try again.")
    
      

if __name__ == "__main__":
    investment()
    with st.expander('View Investments'):
            show_investments()
        