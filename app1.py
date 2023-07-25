import pandas as pd
import numpy as np
import streamlit as st
from tabulate import tabulate
from IPython.display import display, Markdown
import base64
from io import BytesIO

# @st.cache(allow_output_mutation=True)
# df = pd.read_excel("FF 2018 (1).xlsb", engine = "pyxlsb")

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_excel("FF 2018 (1).xlsb", engine="pyxlsb")
    return df
df = load_data()

# Function to get the top exporters
def get_top_exporters(num_exporters):
    top_exporters = df.groupby('IndianCompany')['FOB INR'].sum().nlargest(num_exporters).reset_index()
    top_exporters['FOB INR'] = top_exporters['FOB INR'].apply(lambda x: f"{x:,.2f}")
    exporters_data = top_exporters.values.tolist()
    return exporters_data

# Function to display the top exporters
def top_exporters_page():
    st.title("Top Exporters")
    num_exporters = st.number_input("Enter the number of top exporters to display:", min_value=0, value=0)
    
    exporters_data = get_top_exporters(num_exporters)
    df_exporters = pd.DataFrame(exporters_data, columns=["Exporter", "FOB INR"])
    
    st.markdown("### Top Exporters")
    st.dataframe(df_exporters)

    # Download button
    excel_exporters = BytesIO()
    with pd.ExcelWriter(excel_exporters, engine="xlsxwriter") as writer:
        df_exporters.to_excel(writer, index=False)
    excel_exporters.seek(0)
    b64_exporters = base64.b64encode(excel_exporters.read()).decode()
    href_exporters = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_exporters}" download="top_exporters.xlsx">Download as Excel File</a>'
    st.markdown(href_exporters, unsafe_allow_html=True)


# Function to get the top importers
def get_top_importers(num_importers):
    top_importers = df.groupby('ForeignCompany')['FOB INR'].sum().nlargest(num_importers).reset_index()
    top_importers['FOB INR'] = top_importers['FOB INR'].apply(lambda x: f"{x:,.2f}")
    importers_data = top_importers.values.tolist()
    return importers_data

# Function to display the top importers
def top_importers_page():
    st.title("Top Importers")
    num_importers = st.number_input("Enter the number of top importers to display:", min_value=0, value=0)
    
    importers_data = get_top_importers(num_importers)
    df_importers = pd.DataFrame(importers_data, columns=["Importer", "FOB INR"])
    
    st.markdown("### Top Importers")
    st.dataframe(df_importers)

    # Download Button
    excel_importers = BytesIO()
    with pd.ExcelWriter(excel_importers, engine="xlsxwriter") as writer:
        df_importers.to_excel(writer, index=False)
    excel_importers.seek(0)
    b64_importers = base64.b64encode(excel_importers.read()).decode()
    href_importers = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_importers}" download="top_importers.xlsx">Download as Excel File</a>'
    st.markdown(href_importers, unsafe_allow_html=True)

def get_top_products(num_products):
    top_products = df.groupby('Product')['FOB INR'].sum().nlargest(num_products)
    products_data = [[product, f"{inr:,.2f}"] for product, inr in zip(top_products.index, top_products.values)]
    return products_data

    # Download button
    excel_products = BytesIO()
    with pd.ExcelWriter(excel_products, engine="xlsxwriter") as writer:
        df_products.to_excel(writer, index=False)
    excel_products.seek(0)
    b64_products = base64.b64encode(excel_products.read()).decode()
    href_products = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_products}" download="top_products.xlsx">Download as Excel File</a>'
    st.markdown(href_products, unsafe_allow_html=True)

    

# Function to display the top products
def top_products_page():
    st.title("Top Products")
    num_products = st.number_input("Enter the number of top products to display:", min_value=0, value=0)
    
    products_data = get_top_products(num_products)
    df_products = pd.DataFrame(products_data, columns=["Product", "FOB INR"])
    df_products = df_products.sort_values('FOB INR', ascending=False)  # Sort by FOB INR
    
    st.markdown("### Top Products")
    st.dataframe(df_products)

    # Download button
    excel_products = BytesIO()
    with pd.ExcelWriter(excel_products, engine="xlsxwriter") as writer:
        df_products.to_excel(writer, index=False)
    excel_products.seek(0)
    b64_products = base64.b64encode(excel_products.read()).decode()
    href_products = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_products}" download="top_products.xlsx">Download as Excel File</a>'
    st.markdown(href_products, unsafe_allow_html=True)

# def get_top_products(num_products):
#     top_products = df.groupby('Product')['FOB INR'].sum().nlargest(num_products)
#     products_data = [[product, f"{inr:,.2f}"] for product, inr in zip(top_products.index, top_products.values)]
#     return products_data

# # Function to display the top products
# def top_products_page():
#     st.title("Top Products")
#     num_products = st.number_input("Enter the number of top products to display:", min_value=0, value=0)
    
#     products_data = get_top_products(num_products)
#     df_products = pd.DataFrame(products_data, columns=["Product", "FOB INR"])
#     df_products = df_products.sort_values('FOB INR', ascending=False)  # Sort by FOB INR
#     df_products = df_products.reset_index(drop=True)  # Reset the index
    
#     st.markdown("### Top Products")
#     st.dataframe(df_products)


# Function to display top products by country
def display_top_products_by_country_page():
    st.title("Top Products by Country")
    num_countries = st.number_input("Enter the number of countries:", min_value=0, value=0)
    num_products = st.number_input("Enter the number of products:", min_value=0, value=0)
    
    grouped_data = df.groupby(['ForeignCountry', 'Product'])['FOB INR'].sum(numeric_only=True).reset_index()
    top_countries = grouped_data.groupby('ForeignCountry')['FOB INR'].sum().nlargest(num_countries).index
    
    st.markdown("### Top Products by Country")
    
    for country in top_countries:
        st.markdown(f"#### {country}")
        products = grouped_data[grouped_data['ForeignCountry'] == country].nlargest(num_products, 'FOB INR')
        products = products[['Product', 'FOB INR']]
        st.dataframe(products)
        
        # Download button for each country
        excel_products_by_country = BytesIO()
        with pd.ExcelWriter(excel_products_by_country, engine="xlsxwriter") as writer:
            products.to_excel(writer, index=False)
        excel_products_by_country.seek(0)
        b64_products_by_country = base64.b64encode(excel_products_by_country.read()).decode()
        href_products_by_country = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_products_by_country}" download="top_products_{country.replace(" ", "_")}.xlsx">Download {country} Products as Excel File</a>'
        st.markdown(href_products_by_country, unsafe_allow_html=True)

# Function to display top foreign companies
def display_top_foreign_companies_page():
    st.title("Top Foreign Companies")
    num_companies = st.number_input("Enter the number of foreign companies:", min_value=0, value=0)
    
    top_companies = df.groupby('ForeignCompany')['FOB INR'].sum().nlargest(num_companies).reset_index()
    top_companies['FOB INR'] = top_companies['FOB INR'].apply(lambda x: f"{x:,.2f}")
    
    st.markdown("### Top Foreign Companies")
    st.dataframe(top_companies)

    # Download button
    excel_top_companies = BytesIO()
    with pd.ExcelWriter(excel_top_companies, engine="xlsxwriter") as writer:
        top_companies.to_excel(writer, index=False)
    excel_top_companies.seek(0)
    b64_top_companies = base64.b64encode(excel_top_companies.read()).decode()
    href_top_companies = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_top_companies}" download="top_foreign_companies.xlsx">Download as Excel File</a>'
    st.markdown(href_top_companies, unsafe_allow_html=True)
# # Function to search for an exporter
# def search_exporter_page():
#     st.title("Search Exporter")
#     exporter_name = st.text_input("Enter the exporter name:")
    
#     exporter_data = df[df['IndianCompany'].str.contains(exporter_name, case=False)]
    
#     if len(exporter_data) > 0:
#         st.markdown(f"### Exporter: {exporter_name}")
#         st.dataframe(exporter_data)
#     else:
#         st.markdown("Exporter not found.")

# # Function to search for an importer
# def search_importer_page():
#     st.title("Search Importer")
#     importer_name = st.text_input("Enter the importer name:")
    
#     importer_data = df[df['ForeignCompany'].str.contains(importer_name, case=False)]
    
#     if len(importer_data) > 0:
#         st.markdown(f"### Importer: {importer_name}")
#         st.dataframe(importer_data)
#     else:
#         st.markdown("Importer not found.")

# Function to search for an exporter
# def search_exporter_page():
#     st.title("Search Exporter")
#     exporter_name = st.text_input("Enter the exporter name:")
    
#     if exporter_name:
#         exporter_data = df[df['IndianCompany'].str.contains(exporter_name, case=False)]
    
#         if len(exporter_data) > 0:
#             st.markdown(f"### Exporter: {exporter_name}")
#             st.dataframe(exporter_data)
#         else:
#             st.markdown("Exporter not found.")

def search_exporter_page(df):
    st.title("Search Exporter")
    exporter_name = st.text_input("Enter the Indian exporter:")

    if exporter_name:
        # Check if the input exporter is in the DataFrame
        if exporter_name in df['IndianCompany'].unique():
            # Filter the DataFrame for the selected exporter
            filtered_df = df[df['IndianCompany'] == exporter_name]

            # Group the data by Foreign Company and Foreign Country
            grouped_data = filtered_df.groupby(['ForeignCompany', 'ForeignCountry']).agg({'FOB INR': 'sum'}).reset_index()

            # Sort the data by FOB INR column in descending order
            grouped_data = grouped_data.sort_values('FOB INR', ascending=False)

            # Calculate and display the total FOB INR for all transactions
            total_fob_inr = grouped_data['FOB INR'].sum()

            # Display the results in a tabular format
            table_data = grouped_data.values.tolist()
            headers = ['Foreign Company', 'Foreign Country', 'FOB INR']

            # Format FOB INR values with commas and 2 decimal places
            formatted_table_data = [[company, country, f"{inr:,.2f}"] for company, country, inr in table_data]

            st.markdown("### Export Details")
            st.markdown(f"#### Indian Exporter: {exporter_name}")
            st.markdown(tabulate(formatted_table_data, headers=headers, tablefmt='pipe'))

            # Display the total FOB INR for all transactions without scientific notation
            st.markdown(f"Total FOB INR for all transactions: {format(total_fob_inr, ',')}")
        else:
            st.markdown("Invalid Indian exporter. Please enter a valid exporter.")
    else:
        filtered_df = pd.DataFrame()  # Create an empty DataFrame when exporter_name is not entered
    
    # Download button
    excel_exporter = BytesIO()
    with pd.ExcelWriter(excel_exporter, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False)
    excel_exporter.seek(0)
    b64_exporter = base64.b64encode(excel_exporter.read()).decode()
    href_exporter = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_exporter}" download="exporter_details.xlsx">Download as Excel File</a>'
    st.markdown(href_exporter, unsafe_allow_html=True)

def search_importer_page(df, foreign_company):
    st.title("Search Importer")
    foreign_company_name = st.text_input("Enter the foreign company:")

    if foreign_company_name:
        # Check if the input importer is in the DataFrame
        if foreign_company_name in df['ForeignCompany'].unique():
            # Filter the DataFrame for the selected importer
            filtered_df = df[df['ForeignCompany'] == foreign_company_name]

            # Get the number of Indian companies associated with the foreign company
            num_indian_companies = len(filtered_df['IndianCompany'].unique())

            # Get the list of Indian companies and corresponding FOB INR values associated with the foreign company
            indian_companies = filtered_df['IndianCompany'].unique().tolist()
            fob_inr_values = filtered_df.groupby('IndianCompany')['FOB INR'].sum().tolist()

            # Create a DataFrame for Indian companies and FOB INR
            table_data = {'IndianCompany': indian_companies, 'FOB INR': fob_inr_values}
            df_importer = pd.DataFrame(table_data)

            # Sort the DataFrame by FOB INR column in descending order
            df_importer = df_importer.sort_values('FOB INR', ascending=False)

            # Format FOB INR values with commas and 2 decimal places
            df_importer['FOB INR'] = df_importer['FOB INR'].apply(lambda x: f"{x:,.2f}")

            st.markdown("### Import Details")
            st.markdown(f"#### Foreign Importer: {foreign_company_name}")
            st.markdown(f"Number of Indian Companies associated with {foreign_company_name}: {num_indian_companies}")
            st.markdown("List of Indian Companies and FOB INR:")
            st.markdown(df_importer.to_markdown(index=False))
        else:
            st.markdown("Invalid foreign importer. Please enter a valid importer.")
    
    else:
        df_importer = pd.DataFrame()  # Create an empty DataFrame when foreign_company_name is not entered
    
    # Download button
    excel_importer = BytesIO()
    with pd.ExcelWriter(excel_importer, engine="xlsxwriter") as writer:
        df_importer.to_excel(writer, index=False)
    excel_importer.seek(0)
    b64_importer = base64.b64encode(excel_importer.read()).decode()
    href_importer = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_importer}" download="importer_details.xlsx">Download as Excel File</a>'
    st.markdown(href_importer, unsafe_allow_html=True)
# Function to search for an importer
# def search_importer_page():
#     st.title("Search Importer")
#     importer_name = st.text_input("Enter the importer name:")
    
#     if importer_name:
#         importer_data = df[df['ForeignCompany'].str.contains(importer_name, case=False)]
    
#         if len(importer_data) > 0:
#             st.markdown(f"### Importer: {importer_name}")
#             st.dataframe(importer_data)
#         else:
#             st.markdown("Importer not found.")

# Function to search for a product
def search_product_page(df):
    st.title("Search Product")
    product_name = st.text_input("Enter the product name:")
    
    if product_name:
        # Check if the input product name is in the DataFrame
        if df['Product'].str.contains(product_name, case=False).any():
            # Filter the DataFrame for the selected product
            filtered_df = df[df['Product'].str.contains(product_name, case=False)]

            # Group the data by Foreign Company
            grouped_data = filtered_df.groupby(['ForeignCompany'])['FOB INR'].sum().reset_index()

            # Sort the data by FOB INR column in descending order
            grouped_data = grouped_data.sort_values('FOB INR', ascending=False)

            # Display the results in a tabular format
            table_data = grouped_data.values.tolist()
            headers = ['Foreign Company', 'FOB INR']

            # Format FOB INR values with commas and 2 decimal places
            formatted_table_data = [[company, f"{inr:,.2f}"] for company, inr in table_data]

            st.markdown("### Product Details")
            st.markdown(f"#### Product Name: {product_name}")
            st.markdown(tabulate(formatted_table_data, headers=headers, tablefmt='pipe'))
        else:
            st.markdown("Product not found.")
    else:
        filtered_df = pd.DataFrame()  # Create an empty DataFrame when product_name is not entered
    
    # Download button
    excel_product = BytesIO()
    with pd.ExcelWriter(excel_product, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False)
    excel_product.seek(0)
    b64_product = base64.b64encode(excel_product.read()).decode()
    href_product = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_product}" download="product_details.xlsx">Download as Excel File</a>'
    st.markdown(href_product, unsafe_allow_html=True)


def main():
    st.title("Nutriva Lifesciences")
    st.markdown("### Welcome to the Nutriva Lifesciences Analysis App!")

    pages = {
        "Top Exporters": top_exporters_page,
        "Top Importers": top_importers_page,
        "Top Products": top_products_page,
        "Top Products by Country": display_top_products_by_country_page,
        "Top Foreign Companies": display_top_foreign_companies_page,
        "Search Exporter": lambda: search_exporter_page(df),
        "Search Importer": lambda: search_importer_page(df, "foreign_company"),
        "Search Product": lambda: search_product_page(df)
    }




    # Add a sidebar to the app
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Execute the selected page function
    pages[selection]()

if __name__ == "__main__":
    main()
