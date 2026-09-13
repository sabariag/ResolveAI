import streamlit as st
import requests

st.set_page_config(
    page_title="ResolveAI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 ResolveAI")
st.subheader("Autonomous Customer Resolution Agent")

st.write(
    "Describe your customer issue and let ResolveAI investigate "
    "and find the best resolution."
)

query = st.text_area(
    "Customer Issue",
    placeholder="Example: My headphones arrived damaged. I want a replacement.",
    height=150
)

user_id = st.text_input(
    "User ID (Optional)",
    placeholder="Example: user123"
)

if st.button("Resolve Issue", type="primary"):
    if not query.strip():
        st.warning("Please enter a customer issue.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/resolve",
                json={
                    "query": query,
                    "user_id": user_id
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                st.success(data["result"]["status"])
                st.write(data["result"]["message"])

            else:
                st.error("Failed to connect to ResolveAI backend.")

        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection error: {e}")