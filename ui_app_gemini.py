import streamlit as st
import requests
BACKEND_URL = "http://127.0.0.1:5000/api/ask"

st.title("Q&A Bot")
user_question = st.text_input("Ask a question:", key="question_input")

if st.button("Get Answer"):
    if user_question:
        try:
            payload = {"question": user_question}
            with st.spinner('Thinking...'):
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success("Here's your answer:")
                    st.write(data.get("answer", "No answer found."))
                else:
                    error_data = response.json()
                    st.error(f"Error from server: {error_data.get('error', 'Unknown error')}")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not connect to the Flask backend. Is it running?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a question.")