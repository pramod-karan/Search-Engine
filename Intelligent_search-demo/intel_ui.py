import streamlit as st
import requests

# Function to simulate search and return the predefined output
def perform_search(query,exact):
    PARAMS = {'query':query, "exact":exact}
    result = requests.get(url = "http://localhost:5000/search", params = PARAMS)
    return result.json()

# Streamlit UI Layout
st.title("My Search")
query = st.text_input("Enter your search query:")
exact =st.radio("Exact Search:",("true", "false"),horizontal=True)
if st.button("Search"):
    result = perform_search(query,exact)

    if result["results"]:
        for index, item in enumerate(result["results"]):
            file_name = item['_source']["filename"]
            file_path =  item['_source']["file_path"]
            with st.expander(file_name):
                st.text(item['_source']["parsed_content"])
    else:
        st.error("No results found with the query : {}".format(query))

