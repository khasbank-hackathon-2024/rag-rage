import os
import base64
import streamlit as st
import html
import re
from langchain.callbacks.base import BaseCallbackHandler

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

def format_message(text):
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)
    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text

class StreamlitUICallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.token_buffer = []
        self.placeholder = st.empty()
        self.has_streaming_ended = False
        self.has_streaming_started = False

        self.avatar_base64 = encode_image(os.path.join(os.path.dirname(__file__), "bot.png"))

    def start_loading_message(self):
        loading_message_content = self._get_bot_message_container("Thinking...")
        self.placeholder.markdown(loading_message_content, unsafe_allow_html=True)

    def _get_bot_message_container(self, text):
        formatted_text = format_message(text)
        return f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: flex-start;">
            <img src="data:image/png;base64,{self.avatar_base64}" class="bot-avatar" alt="avatar" style="width: 30px; height: 30px;" />
            <div style="background: #71797E; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; margin-left: 5px; max-width: 75%; font-size: 14px;">
                {formatted_text}
            </div>
        </div>
        """

    def display_dataframe(self, df):
        st.write(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: flex-start;">
            <img src="data:image/png;base64,{self.avatar_base64}" class="bot-avatar" alt="avatar" style="width: 30px; height: 30px;" />
        </div>
        """, unsafe_allow_html=True)
        st.write(df)

    def message_func(self, text, is_user=False):
        base_dir = os.path.dirname(__file__)
        avatar_path = os.path.join(base_dir, "user.png") if is_user else os.path.join(base_dir, "bot.png")
        avatar_base64 = encode_image(avatar_path)

        message_alignment = "flex-end" if is_user else "flex-start"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)" if is_user else "#71797E"
        avatar_class = "user-avatar" if is_user else "bot-avatar"

        formatted_text = format_message(text) 

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                <img src="data:image/png;base64,{avatar_base64}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin: 5px; max-width: 75%; font-size: 14px;">
                    {formatted_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
