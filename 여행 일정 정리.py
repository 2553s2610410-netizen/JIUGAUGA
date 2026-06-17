import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="AI 여행 일정 생성기",
    page_icon="✈️",
    layout="wide"
)

# 관광지 데이터
TOURIST_SPOTS = {
    "서울": [
        "경복궁",
        "북촌한옥마을",
        "인사동",
        "남산타워",
        "명동",
        "한강공원"
    ],
    "부산": [
        "해운대",
        "광안리",
        "감천문화마을",
        "자갈치시장",
        "태종대",
        "송도해상케이블카"
    ],
    "제주": [
        "성산일출봉",
        "섭지코지",
        "우도",
        "협재해수욕장",
        "한라산",
        "천지연폭포"
    ],
    "도쿄": [
        "시부야",
        "신주쿠",
        "아사쿠사",
        "우에노공원",
        "도쿄타워",
        "긴자"
    ],
    "오사카": [
        "도톤보리",
        "오사카성",
        "신세카이",
        "우메다",
        "난바",
        "유니버설 스튜디오 재팬"
    ],
    "파리": [
        "에펠탑",
        "루브르 박물관",
        "개선문",
        "몽마르트르",
        "오르세 미술관",
        "샹젤리제 거리"
    ]
}


def generate_schedule(destination, days):
    places = TOURIST_SPOTS.get(destination, [])

    if not places:
        return pd.DataFrame()

    schedule = []

    place_index = 0

    for day in range(days):

        morning = (
            places[place_index]
            if place_index < len(places)
            else "-"
        )
        place_index += 1

        afternoon = (
            places[place_index]
            if place_index < len(places)
            else "-"
        )
        place_index += 1

        evening = (
            places[place_index]
            if place_index < len(places)
            else "자유시간"
        )
        place_index += 1

        schedule.append({
            "DAY": day + 1,
            "오전": morning,
            "오후": afternoon,
            "저녁": evening
        })

    return pd.DataFrame(schedule)


st.title("✈️ AI 여행 일정 생성기")

st.write(
    "여행지와 여행 기간을 입력하면 자동으로 일정을 만들어드립니다."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input(
        "여행지",
        placeholder="서울, 부산, 제주, 도쿄, 오사카, 파리"
    )

with col2:
    days = st.number_input(
        "여행 일수",
        min_value=1,
        max_value=14,
        value=3
    )

start_date = st.date_input(
    "출발일",
    value=date.today()
)

if st.button("🚀 일정 생성", use_container_width=True):

    if not destination:
        st.warning("여행지를 입력해주세요.")
        st.stop()

    schedule_df = generate_schedule(destination, days)

    if schedule_df.empty:
        st.info(
            "해당 여행지 데이터가 없습니다.\n\n"
            "관광지 추천을 제공할 수 없습니다."
        )
        st.stop()

    st.success("일정 생성 완료!")

    st.subheader("📍 추천 관광지")

    for place in TOURIST_SPOTS[destination]:
        st.write(f"✔ {place}")

    st.subheader("🗓 자동 생성 일정")

    result_rows = []

    for idx, row in schedule_df.iterrows():

        trip_date = start_date + timedelta(days=idx)

        result_rows.append({
            "날짜": trip_date.strftime("%Y-%m-%d"),
            "오전": row["오전"],
            "오후": row["오후"],
            "저녁": row["저녁"]
        })

    result_df = pd.DataFrame(result_rows)

    st.dataframe(
        result_df,
        use_container_width=True
    )

    csv = result_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 일정 CSV 다운로드",
        csv,
        "travel_schedule.csv",
        "text/csv"
    )

    st.subheader("📋 여행 요약")

    st.info(
        f"""
여행지 : {destination}

여행 기간 : {days}일

총 추천 관광지 : {len(TOURIST_SPOTS[destination])}곳
"""
    )
