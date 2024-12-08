import streamlit as st
from rag_chain import create_rag_chain, OPENAI_API_KEY
from utils.ui import  StreamlitUICallbackHandler


st.set_page_config(
    page_title="meic",
    page_icon="utils/logo.png",
    layout="centered",
    initial_sidebar_state="auto"
)

with open("ui/sidebar.md", "r", encoding="utf8") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.image("utils/logo.png", use_column_width=False, width=150)
st.sidebar.markdown(sidebar_content)
st.write(styles_content, unsafe_allow_html=True)


if st.sidebar.button("Ахин эхлүүүлэх"):
    st.session_state.clear()
    st.session_state["messages"] = [{"role": "assistant", "content": "Сайн байна уу танд юугаар туслах вэ?"}]
    st.session_state["history"] = []

callback_handler = StreamlitUICallbackHandler()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Сайн байна уу танд юугаар туслах вэ?"}]

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        callback_handler.message_func(msg["content"], is_user=True)
    else:
        callback_handler.message_func(msg["content"], is_user=False)

# Cache data & RAG
# @st.cache_data
# def get_docs():
#     return load_data()

@st.cache_resource
def get_rag_chain():
    embedding_model = "text-embedding-ada-002"
    db_path = "data/df_emb.pkl"

    chatbot = create_rag_chain(db_path,
                               openai_key=OPENAI_API_KEY,
                               top_k=75,
                               embedding_model=embedding_model)

    return chatbot

if prompt := st.chat_input(placeholder="Та асуух зүйлээ бичнэ үү"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    callback_handler.message_func(prompt, is_user=True)
    chatbot = get_rag_chain()
    answer = chatbot.get_response(query=str(prompt))
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    callback_handler.message_func(answer, is_user=False)