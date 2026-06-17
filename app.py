import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="여행 일정 정리표",
    page_icon="✈️",
    layout="wide"
)

# 관광지 추천 데이터
TOURIST_SPOTS = {
    "서울": [
        "경복궁",
        "북촌한옥마을",
        "남산타워",
        "명동",
        "한강공원"
    ],
    "부산": [
        "해운대",
        "광안리",
        "감천문화마을",
        "태종대",
        "자갈치시장"
    ],
    "제주": [
        "성산일출봉",
        "협재해수욕장",
        "한라산",
        "우도",
        "천지연폭포"
    ],
    "도쿄": [
        "시부야",
        "아사쿠사",
        "도쿄타워",
        "신주쿠",
        "우에노공원"
    ],
    "오사카": [
        "도톤보리",
        "오사카성",
        "유니버설 스튜디오 재팬",
        "신세카이",
        "우메다 스카이빌딩"
    ],
    "파리": [
        "에펠탑",
        "루브르 박물관",
        "개선문",
        "몽마르트르",
        "오르세 미술관"
    ]
}


def get_recommendations(destination):
    destination = destination.strip()

    for city, spots in TOURIST_SPOTS.items():
        if city.lower() == destination.lower():
            return spots

    return []


st.title("✈️ 여행 일정 정리표")

st.write("여행 정보를 입력하면 일정표와 관광지 추천을 제공합니다.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input(
        "여행지 입력",
        placeholder="예: 서울, 부산, 제주, 도쿄, 파리"
    )

with col2:
    traveler = st.text_input(
        "여행자 이름",
        placeholder="홍길동"
    )

col3, col4 = st.columns(2)

with col3:
    start_date = st.date_input(
        "출발일",
        value=date.today()
    )

with col4:
    end_date = st.date_input(
        "도착일",
        value=date.today() + timedelta(days=2)
    )

memo = st.text_area(
    "여행 메모",
    placeholder="준비물, 예약 정보 등을 기록하세요."
)

st.divider()

st.subheader("📍 추천 관광지")

if destination:
    recommendations = get_recommendations(destination)

    if recommendations:
        for spot in recommendations:
            st.success(f"✔ {spot}")
    else:
        st.info("등록된 추천 관광지가 없습니다.")

st.divider()

st.subheader("🗓 여행 일정표")

try:
    if end_date < start_date:
        st.error("도착일은 출발일보다 빠를 수 없습니다.")
    else:
        total_days = (end_date - start_date).days + 1

        schedule_data = []

        for i in range(total_days):
            current_day = start_date + timedelta(days=i)

            schedule_data.append({
                "날짜": current_day,
                "오전 일정": "",
                "오후 일정": "",
                "저녁 일정": ""
            })

        schedule_df = pd.DataFrame(schedule_data)

        edited_df = st.data_editor(
            schedule_df,
            use_container_width=True,
            num_rows="fixed"
        )

        csv = edited_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="📥 일정표 CSV 다운로드",
            data=csv,
            file_name="travel_schedule.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

st.divider()

st.subheader("📋 여행 요약")

st.write(f"**여행자:** {traveler if traveler else '-'}")
st.write(f"**여행지:** {destination if destination else '-'}")

if end_date >= start_date:
    days = (end_date - start_date).days + 1
    st.write(f"**여행 기간:** {days}일")

st.write(f"**메모:** {memo if memo else '-'}")
