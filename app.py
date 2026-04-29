import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

from scraper import scrape_page_text
from ai_extractor import extract_incentive_data
from validator import validate_record

load_dotenv()

st.set_page_config(page_title="Dreamline AI Extractor + Chatbot", layout="wide")

st.title("Dreamline AI Incentive Extractor + Chatbot")

# store data
if "page_text" not in st.session_state:
    st.session_state.page_text = ""

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

# ---------------- EXTRACT SECTION ----------------
url = st.text_input("Enter incentive URL")

if st.button("Extract"):
    if url:
        with st.spinner("Extracting..."):
            try:
                text = scrape_page_text(url)
                data = extract_incentive_data(text, url)
                data = validate_record(data)

                st.session_state.page_text = text
                st.session_state.extracted_data = data

                st.success("Extraction done!")

            except Exception as e:
                st.error(e)
    else:
        st.warning("Enter URL first")

# show table
if st.session_state.extracted_data:
    df = pd.DataFrame([st.session_state.extracted_data])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button("Download CSV", csv, "data.csv", "text/csv")

# ---------------- CHATBOT SECTION ----------------
st.divider()
st.subheader("Ask AI about this incentive")

question = st.text_input("Ask your question")

if st.button("Ask"):
    if not st.session_state.page_text:
        st.warning("First extract data")
    elif not question:
        st.warning("Enter question")
    else:
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))

                context = f"""
Data:
{st.session_state.extracted_data}

Text:
{st.session_state.page_text[:6000]}
"""

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Answer based only on given context"},
                        {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
                    ]
                )

                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(e)