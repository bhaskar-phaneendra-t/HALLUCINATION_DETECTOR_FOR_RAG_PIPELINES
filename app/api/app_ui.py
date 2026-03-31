import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Hallucination Firewall", layout="wide")

st.title(" Hallucination Firewall")
st.markdown("Detect hallucinations in LLM responses with real-time validation")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

def format_decision(decision):
    if decision == "SAFE":
        return "🟢 SAFE"
    elif decision == "WARNING":
        return "🟡 WARNING"
    elif decision == "HALLUCINATION":
        return "🔴 HALLUCINATION"
    elif decision == "OUT_OF_SCOPE":
        return "⚪ OUT OF SCOPE"
    elif decision == "NO_CONTEXT":
        return "⚫ NO CONTEXT"
    else:
        return decision


# Input box
query = st.chat_input("Ask your question...")

if query:
    try:
        # Call backend API
        res = requests.post(API_URL, json={"query": query})
        data = res.json()

        final_output = data.get("final_output") or {}

        if isinstance(final_output, dict):
            answer = final_output.get("final_answer", "No response available")
            message = final_output.get("message", None)
        else:
            answer = "System error: invalid response"
            message = None

        if message:
            st.info(message)

        decision = data.get("decision", "UNKNOWN")
        score = data.get("hallucination_score", None)

        decision_display = format_decision(decision)

        # Store chat
        st.session_state.history.append({
            "query": query,
            "answer": answer,
            "decision": decision_display,
            "score": score
        })

    except Exception as e:
        st.error(f"Error: {str(e)}")


# Display chat history
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.write(chat["query"])

    with st.chat_message("assistant"):
        st.write(chat.get("answer", "No answer"))
        st.markdown(f"**Decision:** {chat['decision']}")
        st.markdown(f"**Score:** {chat['score']}")