# chat/views.py

import os
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from code_final.api_test import synthesize
from code_final.rag_chain import create_rag_chain, OPENAI_API_KEY
# from utils.ui import StreamlitUICallbackHandler  # Not needed
# Module-level variable to store the chatbot
_chatbot = None

def index(request):
    return render(request,'core/index.html')

def get_rag_chain():
    global _chatbot
    if _chatbot is None:
        embedding_model = "text-embedding-ada-002"
        db_path = 'C:/Users/ohusl/hackathon-xac/core/df_emb_new.pkl'
        _chatbot = create_rag_chain(
            db_path,
            openai_key=OPENAI_API_KEY,
            top_k=75,
            embedding_model=embedding_model
        )
    return _chatbot

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        return file.read()

def chat_view(request):
    if 'messages' not in request.session:
        request.session['messages'] = [
            {"role": "assistant", "content": "Сайн байна уу танд юугаар туслах вэ?"}
        ]
        request.session['history'] = []

    messages = request.session.get('messages', [])
  
    context = {
        'messages': messages,
    }
    if request.htmx: 
        return render(request, 'partials/response.html', context)

    return render(request, 'core/chat.html', context)

@require_POST
def send_message(request):
    prompt = request.POST.get('message')
    if prompt:
        messages = request.session.get('messages', [])
        messages.append({"role": "user", "content": prompt})
        request.session['messages'] = messages

        chatbot = get_rag_chain()
        answer = chatbot.get_response(query=str(prompt))
        messages.append({"role": "assistant", "content": answer})
        request.session['messages'] = messages



        return render(request, 'partials/response.html', {
            'messages': messages,
            'audio_url': audio_url,
        })

    return redirect('chat')


@require_POST
def reset_chat(request):
    request.session.flush()
    return redirect('chat')
