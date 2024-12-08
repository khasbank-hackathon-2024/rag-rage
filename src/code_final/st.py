import streamlit as st
from data_load import load_data
from rag_chain import create_rag_chain


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Сайн байна уу таньд юугаар туслах вэ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

@st.cache_data
def get_docs():
    return load_data()

@st.cache_resource
def get_rag_chain():
    docs = get_docs()
    return create_rag_chain(docs)


if prompt := st.chat_input(placeholder="Та асуух зүйлээ бичнэ үү"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    rag_chain = get_rag_chain()
    response = rag_chain.invoke({"input": prompt})
    answer = response["answer"]
    #print(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
