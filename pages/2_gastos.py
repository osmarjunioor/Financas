#python -m streamlit run 1_Links.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Portal de Gastos e Finanças")

# Constants
BUSINESS_TYPES = [
    "Mercado",
    "Shopping",
    "Restaurante",
    "Loja",
    "Construção",
    "Outros",
]
PRODUCTS = [
    "Electronicos",
    "Roupa",
    "Comida",
    "Construção",
    "Outros",
]

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

action = st.selectbox(
    "Escolha uma Ação",
    [
        "Adicione Gastos",
        "Update Existing Vendor",
        "View All Vendors",
        "Delete Vendor",
    ],
)

if action == "Adicione Gastos":
    st.markdown("Adicione informações sobre novos gastos.")
    with st.form(key="vendor_form"):
        company_name = st.text_input(label="Nome do local*")
        business_type = st.selectbox(
            "Tipo do Local*", options=BUSINESS_TYPES, index=None
        )
        products = st.multiselect("Produto Comprado", options=PRODUCTS)
        years_in_business = st.slider("Years in Business", 0, 50, 5)
        onboarding_date = st.date_input(label="Data da Compra")
        additional_info = st.text_area(label="Observações")

        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Submit Vendor Details")

        if submit_button:
            if not company_name or not business_type:
                st.warning("Ensure all mandatory fields are filled.")
            elif existing_data["CompanyName"].str.contains(company_name).any():
                st.warning("A vendor with this company name already exists.")
            else:
                vendor_data = pd.DataFrame(
                    [
                        {
                            "CompanyName": company_name,
                            "BusinessType": business_type,
                            "Products": ", ".join(products),
                            "YearsInBusiness": years_in_business,
                            "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                            "AdditionalInfo": additional_info,
                        }
                    ]
                )
                updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
                conn.update(worksheet="Vendors", data=updated_df)
                st.success("Vendor details successfully submitted!")

elif action == "Update Existing Vendor":
    st.markdown("Select a vendor and update their details.")

    vendor_to_update = st.selectbox(
        "Select a Vendor to Update", options=existing_data["CompanyName"].tolist()
    )
    vendor_data = existing_data[existing_data["CompanyName"] == vendor_to_update].iloc[
        0
    ]

    with st.form(key="update_form"):
        company_name = st.text_input(
            label="Company Name*", value=vendor_data["CompanyName"]
        )
        business_type = st.selectbox(
            "Business Type*",
            options=BUSINESS_TYPES,
            index=BUSINESS_TYPES.index(vendor_data["BusinessType"]),
        )
        products = st.multiselect(
            "Products Offered",
            options=PRODUCTS,
            default=vendor_data["Products"].split(", "),
        )
        years_in_business = st.slider(
            "Years in Business", 0, 50, int(vendor_data["YearsInBusiness"])
        )
        onboarding_date = st.date_input(
            label="Data da Compra", value=pd.to_datetime(vendor_data["OnboardingDate"])
        )
        additional_info = st.text_area(
            label="Observações", value=vendor_data["AdditionalInfo"]
        )

        st.markdown("**required*")
        update_button = st.form_submit_button(label="Update Vendor Details")

        if update_button:
            if not company_name or not business_type:
                st.warning("Ensure all mandatory fields are filled.")
            else:
                # Removing old entry
                existing_data.drop(
                    existing_data[
                        existing_data["CompanyName"] == vendor_to_update
                    ].index,
                    inplace=True,
                )
                # Creating updated data entry
                updated_vendor_data = pd.DataFrame(
                    [
                        {
                            "CompanyName": company_name,
                            "BusinessType": business_type,
                            "Products": ", ".join(products),
                            "YearsInBusiness": years_in_business,
                            "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                            "AdditionalInfo": additional_info,
                        }
                    ]
                )
                # Adding updated data to the dataframe
                updated_df = pd.concat(
                    [existing_data, updated_vendor_data], ignore_index=True
                )
                conn.update(worksheet="Vendors", data=updated_df)
                st.success("Vendor details successfully updated!")

# View All Vendors
elif action == "View All Vendors":
    st.dataframe(existing_data)

# Delete Vendor
elif action == "Delete Vendor":
    vendor_to_delete = st.selectbox(
        "Select a Vendor to Delete", options=existing_data["CompanyName"].tolist()
    )

    if st.button("Delete"):
        existing_data.drop(
            existing_data[existing_data["CompanyName"] == vendor_to_delete].index,
            inplace=True,
        )
        conn.update(worksheet="Vendors", data=existing_data)
        st.success("Vendor successfully deleted!")
