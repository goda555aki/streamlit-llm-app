
from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

st.title("専門家に聞いてみよう！")

option = st.radio("質問したいテーマを選んでください", ("今日の献立", "週末の温泉"))

# OpenAI APIキーの取得
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_expert_response(role, user_input):
    if not openai_api_key:
        return "APIキーが設定されていません。"
    if role == "料理研究家":
        system_prompt = "あなたは日本の料理研究家です。食材や気分に合わせて献立を提案してください。"
    else:
        system_prompt = "あなたは温泉ソムリエです。エリアや希望に合わせておすすめの温泉地を提案してください。"
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o", temperature=0.7)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    return llm(messages).content

if option == "今日の献立":
    ingredient = st.text_input("使いたい食材や気分を入力してください")
    if st.button("料理研究家に質問する") and ingredient:
        with st.spinner("料理研究家が考え中..."):
            response = get_expert_response("料理研究家", ingredient)
            st.markdown("### 料理研究家の回答")
            st.success(response)
elif option == "週末の温泉":
    location = st.text_input("行きたいエリアや都道府県を入力してください")
    if st.button("温泉ソムリエに質問する") and location:
        with st.spinner("温泉ソムリエが考え中..."):
            response = get_expert_response("温泉ソムリエ", location)
            st.markdown("### 温泉ソムリエの回答")
            st.success(response)
        
