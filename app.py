import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

library_rules = """
제20조(휴관일)
1. 자료실: 공휴일, 개교기념일
2. 일반열람실: 설날, 추석

제22조(대출책수 및 기간)
1. 전임교원, 겸임교원, 명예교수, 강사: 50책 이내 90일
2. 직원, 조교, 대학원생: 20책 이내 30일
3. 학부생: 10책 이내 14일

전자책:
5책 이내, 5일
"""

st.title("국립부경대학교 도서관 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("질문을 입력하세요")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
너는 국립부경대학교 도서관 챗봇이다.

아래 규정만 참고하여 답변하라.

{library_rules}

질문:
{question}
"""
    )

    answer = response.output_text

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

if st.button("Clear"):
    st.session_state.messages = []
    st.rerun()