import requests
import pandas as pd
from time import sleep
import streamlit as st
import numpy as np

st.title('WordPress Post Date Retriever')
st.subheader("Gets post dates from WordPress REST API and saves to CSV")
st.markdown("Publication dates are useful information for content strategists and SEOs, but not all websites make them easy to find. This app was created to get **post publication** and **last modified dates** for WordPress websites with the [REST API](https://developer.wordpress.org/rest-api/) enabled. This is particularly useful for websites where the post dates are not published in the URL or HTML and are not accessible to a website crawler.")

with st.form("inputs"):
    domain = st.text_input(
        "Enter domain", 
        placeholder = "awordpresswebsite.com"
        )
    user_agent = st.text_input(
        "(Optional) Update user agent", 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
        )
    submitted = st.form_submit_button(label="Get posts")

if submitted:
    if domain.endswith("/"):
        domain = domain[:-1]
        
    protocol = "https://"
    path = "/wp-json/wp/v2/posts"

    per_page = 100
    page = 1
    status = "publish"
    fields = "title,link,date,modified"
    params = {
        'per_page': per_page, 
        'page': page,
        'status': status,
        '_fields': fields
    }
    headers = {'User-Agent': user_agent}

    url = protocol + domain + path

    response = requests.request(
        "GET",
        url = url,
        params = params,
        headers = headers
    )

    pages = int(response.headers['X-WP-TotalPages'])
    rows = int(response.headers['X-WP-Total'])
    row_info = st.empty()
    page_info = st.empty()
    row_info.text("Requesting " + str(rows) + " records...")
    bar = st.progress(0)

    def getData():
        data = []
        global page
        while page <= pages:
            params['page'] = page
            response = requests.request(
                "GET",
                url = url,
                params = params,
                headers = headers
            )
            bar.progress(page/pages)
            for i in response.json():
                data.append(i)
            page_info.text("Retrieved " + str(page) + " of " + str(pages) + " pages.")
            page = page + 1
            sleep(1)
        global all_data    
        all_data = pd.json_normalize(data)

        @st.cache 
        def convert_df(all_data):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return all_data.to_csv().encode('utf-8')
        global csv
        csv = convert_df(all_data)
        global file_name
        file_name = str(domain).replace("/","_") + "_all_posts.csv"

    if response.status_code == 200:
        getData()
        row_info.empty()
        page_info.empty()
        st.write(all_data)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=file_name,
            mime='text/csv',
            )
    elif response.status_code == 403:
        print(response.status_code, "error: ensure the user agent variable is set.")
    else:
        print(response.status_code, "error.")
