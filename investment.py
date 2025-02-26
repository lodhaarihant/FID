import streamlit as st
import db as dbt
import pandas as pd
import datetime
import os


st.set_page_config(layout="wide")

def generate_buttons(file_url):
    if pd.isna(file_url) or file_url == "":
        return "No File Available"
    # View button (opens in a new tab)
    file_url = file_url.strip()
    file_url = f"http://localhost:8502/{file_url}"
    view_link = f'<a href="{file_url}" target="_blank" style="color: blue; text-decoration: none;">👁️</a>'
    # Download button
    download_link = f'<a href="{file_url}" download style="color: green; text-decoration: none;">⬇️</a>'
    # Combine both buttons
    return f"{view_link} | {download_link}"

def show_investments():
    st.subheader("View Investment Details", divider="rainbow")
    investments_df = dbt.fetch_all_investments()

    if investments_df.empty:
        st.warning("⚠️ No investments found.")
    else:
        # Apply buttons to a column if "Attachment" column exists
        if "Attachment" in investments_df.columns:
            investments_df["Actions"] = investments_df["Attachment"].apply(generate_buttons)

        # **Display as an interactive table with buttons**
        st.markdown(investments_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        # **Download Button**
        csv = investments_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Investments Data",
            data=csv,
            file_name="investments.csv",
            mime="text/csv",
            key="download_investments_btn"  # Added unique key
        )

             
def investment():
    dbt.create_investment_table()
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("You must log in first!")
        st.stop()
        
        
    with st.expander('Enter Investment Investments', expanded=True):  # Added unique key
        st.subheader("Enter Investment Details", divider='rainbow')
        col1, col2 = st.columns([2, 5])  
        with col1:
            invested_amount = st.number_input("Invested Amount", key="inv_amount",min_value=0,step=1000)  # Added unique key
            investment_date = st.date_input("Investment Date", datetime.date.today(), key="inv_date")  # Added unique key
        with col2:
            maturity_date = st.date_input("Maturity Date", key="maturity_date")  # Added unique key
            attachment = st.file_uploader("Upload Proof (Optional)", type=["pdf", "jpg", "png"], key="inv_attachment")  # Added unique key
        
        if st.button("Submit Investment", key="submit_inv_btn"):  # Added unique key
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
    
    with st.expander('View Investments',expanded=True):  # Added unique key
        show_investments()
      
if __name__ == "__main__":
    investment()
  