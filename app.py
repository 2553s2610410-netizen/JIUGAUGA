import streamlit as st
from datetime import date

st.set_page_config(
    page_title="여행 일정 정리표",
    page_icon="✈️",
    layout="wide"
)

# ----------------------------
# 여행 일정 생성 함수
# ----------------------------
def generate_schedule(destination, days, style):
    schedule = []

    style_templates = {
        "관광": [
            "대표 관광지 방문",
            "유명 랜드마크 탐방",
            "현지 맛집 방문",
            "야경 감상"
        ],
        "휴양": [
            "호텔 및 리조트 휴식",
            "카페 투어",
            "산책 및 힐링",
            "자유 시간"
        ],
        "맛집": [
            "현지 유명 맛집 방문",
            "전통시장 탐방",
            "카페 투어",
            "야식 즐기기"
        ],
        "가족여행": [
            "가족 명소 방문",
            "체험 프로그램 참여",
            "공원 산책",
            "기념사진 촬영"
        ]
    }

    activities = style_templates.get(style, style_templates["관광"])

    for day in range(1, days + 1):
        schedule.append({
            "day": day,
            "morning": activities[0],
            "afternoon": activities[1],
            "evening": activities[2],
            "night": activities[3]
        })

    return schedule


# ----------------------------
# 준비물 생성
# ----------------------------
def get_checklist(style):
    base = [
        "여권/신분증",
        "휴대폰 충전기",
        "보조배터리",
        "현금 및 카드",
        "세면도구"
    ]

    if style == "휴양":
        base.extend([
            "수영복",
            "선글라스",
            "선크림"
        ])

    elif style == "맛집":
        base.extend([
            "카메라",
            "물티슈"
        ])

    elif style == "가족여행":
        base.extend([
            "상비약",
            "간식"
        ])

    return base


# ----------------------------
# 제목
# ----------------------------
st.title("✈️ 여행 일정 정리표")
st.caption("여행지를 입력하면 자동으로 일정표를 생성합니다.")

# ----------------------------
# 입력 영역
# ----------------------------
with st.form("travel_form"):

    destination = st.text_input(
        "여행지",
        placeholder="예: 제주도, 도쿄, 파리"
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "출발일",
            value=date.today()
        )

    with col2:
        end_date = st.date_input(
            "도착일",
            value=date.today()
        )

    style = st.selectbox(
        "여행 스타일",
        ["관광", "휴양", "맛집", "가족여행"]
    )

    submitted = st.form_submit_button("일정 생성")

# ----------------------------
# 결과
# ----------------------------
if submitted:

    if not destination.strip():
        st.error("여행지를 입력해주세요.")
        st.stop()

    if end_date < start_date:
        st.error("도착일은 출발일 이후여야 합니다.")
        st.stop()

    days = (end_date - start_date).days + 1

    st.success(
        f"{destination} {days}일 여행 일정이 생성되었습니다."
    )

    schedule = generate_schedule(
        destination,
        days,
        style
    )

    st.subheader("📅 여행 일정")

    markdown_text = f"# {destination} 여행 일정\n\n"

    for item in schedule:

        with st.expander(f"{item['day']}일차"):

            st.write(f"🌅 오전 : {item['morning']}")
            st.write(f"☀️ 오후 : {item['afternoon']}")
            st.write(f"🌇 저녁 : {item['evening']}")
            st.write(f"🌙 밤 : {item['night']}")

        markdown_text += (
            f"## {item['day']}일차\n"
            f"- 오전: {item['morning']}\n"
            f"- 오후: {item['afternoon']}\n"
            f"- 저녁: {item['evening']}\n"
            f"- 밤: {item['night']}\n\n"
        )

    st.subheader("🎒 여행 준비물")

    checklist = get_checklist(style)

    for item in checklist:
        st.checkbox(item)

    markdown_text += "\n## 준비물\n"

    for item in checklist:
        markdown_text += f"- {item}\n"

    st.download_button(
        label="📥 일정표 다운로드 (Markdown)",
        data=markdown_text,
        file_name=f"{destination}_travel_plan.md",
        mime="text/markdown"
    )

# ----------------------------
# 안내
# ----------------------------
st.divider()

st.info(
    """
    사용 방법
    1. 여행지를 입력하세요.
    2. 여행 기간을 선택하세요.
    3. 여행 스타일을 선택하세요.
    4. 일정 생성 버튼을 누르세요.
    """
)
