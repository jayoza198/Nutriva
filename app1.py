import pandas as pd
import numpy as np
import streamlit as st
from tabulate import tabulate
from IPython.display import display, Markdown

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

# Function to get the top products
def get_top_products(num_products):
    top_products = df.groupby('Product')['FOB INR'].sum().nlargest(num_products)
    products_data = [[product[:50], count, f"{inr:,.2f}"] for product, count, inr in zip(top_products.index, top_products.values, top_products)]
    return products_data

# Function to display the top products
def top_products_page():
    st.title("Top Products")
    num_products = st.number_input("Enter the number of top products to display:", min_value=0, value=0)
    
    products_data = get_top_products(num_products)
    df_products = pd.DataFrame(products_data, columns=["Product", "FOB INR"])
    
    st.markdown("### Top Products")
    st.dataframe(df_products)

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

# Function to display top foreign companies
def display_top_foreign_companies_page():
    st.title("Top Foreign Companies")
    num_companies = st.number_input("Enter the number of foreign companies:", min_value=0, value=0)
    
    top_companies = df.groupby('ForeignCompany')['FOB INR'].sum().nlargest(num_companies).reset_index()
    top_companies['FOB INR'] = top_companies['FOB INR'].apply(lambda x: f"{x:,.2f}")
    
    st.markdown("### Top Foreign Companies")
    st.dataframe(top_companies)

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
        "Search Importer": lambda: search_importer_page(df, "foreign_company")
    }




    # Add a sidebar to the app
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Execute the selected page function
    pages[selection]()

if __name__ == "__main__":
    main()
