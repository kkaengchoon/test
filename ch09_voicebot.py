# https://github.com/kkaengchoon/test/upload/main
import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
import numpy as np


def STT(audio, apikey):
    filename = 'input.mp3'
    audio.export(filename, format="mp3")

    audio_file = open(filename, "rb")
    client = openai.OpenAI(api_key = apikey)
    respons = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
    audio_file.close()
    os.remove(filename)
    return respons.text

def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.audio.transcriptions.create(
        model = model,
        message = prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse


def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")
    
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENSI_API"] = ""

    if "message" not in st.session_state:
        st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
    
    st.header("음성 비서 프로그램")
    st.markdown("---")

    with st.sidebar:
        st.session_state["OPEN_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")
        st.markdown("---")

        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])
        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("질문하기")
        st.subheader("텍스트 질문하기")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("질문을 작성하세요"):
            st.session_state.messages.append({"role": "user", "content": prompt})

    with col2:
        st.subheader("질문/답변")
        with st.chat_message("user"):
                st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages], stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)



if __name__=="__main__":
    main()