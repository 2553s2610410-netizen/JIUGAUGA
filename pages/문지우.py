import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="AI 일정 생성기",
    page_icon="📅",
    layout="centered"
)

st.title("📅 AI 일정 생성 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 일정 생성 앱")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ secrets.toml에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 👋\n"
                "원하는 일정이나 계획을 알려주시면 "
                "효율적인 스케줄을 만들어드릴게요!\n\n"
                "예시:\n"
                "- 3일 제주도 여행 일정 짜줘\n"
                "- 하루 공부 루틴 만들어줘\n"
                "- 운동 + 식단 일정 짜줘"
            )
        }
    ]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("원하는 일정을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        try:
            # 시스템 프롬프트
            system_prompt = """
            너는 전문 일정 플래너 AI다.

            규칙:
            - 사용자의 목적에 맞는 현실적인 일정 생성
            - 시간 순서대로 정리
            - 가독성 좋게 마크다운 사용
            - 필요하면 표 형태 사용
            - 일정 팁도 함께 제공
            - 한국어로 친절하게 답변
            """

            # Gemini 대화 형식 변환
            contents = []

            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            # Gemini 응답 생성
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                    max_output_tokens=1200,
                )
            )

            bot_reply = response.text

            # 응답 출력
            message_placeholder.markdown(bot_reply)

            # 채팅 기록 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_reply
            })

        except Exception as e:

            error_message = f"""
            ❌ 일정 생성 중 오류가 발생했습니다.

            잠시 후 다시 시도해주세요.

            오류 내용:
            {str(e)}
            """

            message_placeholder.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": "오류가 발생했어요 😢 잠시 후 다시 시도해주세요."
            })
