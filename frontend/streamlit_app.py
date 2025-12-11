import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/rag/query"


def main():
    st.set_page_config(
        page_title="Your personal YouTuber Assistant",
        page_icon="🎥",
        layout="wide",
    )

    st.title("🎥 Your personal YouTuber Assistant")

    st.markdown(
        """
        **Ställ frågor baserat på innehållet i Youtube-matrialet**
        
        Appen använder RAG (Retrieval-Augmented Generation) för att hitta relevant information 
        från transkriberade videor och ger dig svar baserat på datan.
        """
    )

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    # Session state sparar det senaste svaret
    if "last_question" not in st.session_state:
        st.session_state.last_question = None
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
        
    with col_left:
        st.subheader("💬 Fråga assistenten")

        question = st.text_input(
            label="Skriv din fråga här:",
            placeholder="T.ex. 'Vad handlar kursen om?'"
        )

        send_clicked = st.button("🚀 Skicka", type="primary")

        if send_clicked:
            if question.strip() == "":
                st.warning("⚠️ Skriv in en fråga innan du skickar.")
            else:
                st.session_state.last_question = question
                st.session_state.last_response = None

                with st.spinner("🔍 Söker i kunskapsbasen..."):
                    try:
                        response = requests.post(
                            API_URL,
                            json={"prompt": question},
                            timeout=60,
                        )
                    except requests.RequestException as e:
                        st.error(f"❌ Kunde inte kontakta API:t: {e}")
                    else:
                        if not response.ok:
                            try:
                                data = response.json()
                                detail = data.get("detail", response.text)
                            except Exception:
                                detail = response.text

                            st.error(f"❌ API-fel ({response.status_code}): {detail}")
                        else:
                            st.session_state.last_response = response.json()
                            st.success("✅ Svar mottaget!")

        # Visar användarens senaste fråga och svar
        if st.session_state.last_question:
            st.markdown("---")
            st.markdown("### 📝 Din fråga")
            st.info(st.session_state.last_question)

            if st.session_state.last_response:
                data = st.session_state.last_response
                
                st.markdown("### 💡 Svar")
                answer = data.get("answer", "Inget svar returnerades från backend.")
                st.markdown(answer)

    with col_right:
        st.subheader("📚 Källa")

        if st.session_state.get("last_response") is None:
            st.info("När du fått ett svar visas källan här.")
        else:
            data = st.session_state.last_response
            
            file_name = data.get("file_name", "Okänd fil")
            file_path = data.get("file_path", "N/A")

            st.markdown(f"**Fil:** `{file_name}`")
            
            if file_path != "N/A":
                st.markdown(f"**Sökväg:** `{file_path}`")
            
            st.markdown("---")
            st.caption("Svaret baseras på innehållet från denna fil.")


if __name__ == "__main__":
    main()