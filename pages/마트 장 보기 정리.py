import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="마트 장보기 플래너",
    page_icon="🛒",
    layout="wide"
)

shopping_data = {
    "월요일": {
        "신선식품": ["우유", "계란", "두부"],
        "채소": ["상추", "양파", "대파"]
    },
    "화요일": {
        "신선식품": ["요거트", "치즈"],
        "채소": ["오이", "당근"]
    },
    "수요일": {
        "신선식품": ["닭가슴살", "햄"],
        "채소": ["브로콜리", "파프리카"]
    },
    "목요일": {
        "신선식품": ["두유", "버터"],
        "채소": ["감자", "양배추"]
    },
    "금요일": {
        "신선식품": ["소고기", "돼지고기"],
        "채소": ["버섯", "깻잎"]
    },
    "토요일": {
        "간식": ["과자", "아이스크림"],
        "음료": ["주스", "탄산음료"]
    },
    "일요일": {
        "비축용": ["라면", "즉석밥"],
        "생활용품": ["휴지", "세제"]
    }
}

st.title("🛒 마트 장보기 플래너")
st.caption("요일별 추천 장보기 목록을 확인하고 체크하세요.")

st.image(
    "https://images.unsplash.com/photo-1542838132-92c53300491e",
    caption="즐거운 장보기",
    use_container_width=True
)

weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

today = weekday_map[datetime.today().weekday()]

selected_day = st.selectbox(
    "요일 선택",
    list(shopping_data.keys()),
    index=list(shopping_data.keys()).index(today)
)

st.subheader(f"📅 {selected_day} 추천 구매 목록")

total_items = 0
checked_items = 0

for category, items in shopping_data[selected_day].items():
    st.markdown(f"### 🏷️ {category}")

    for item in items:
        total_items += 1

        checked = st.checkbox(
            item,
            key=f"{selected_day}_{category}_{item}"
        )

        if checked:
            checked_items += 1

st.divider()

st.subheader("📊 장보기 진행률")

progress = checked_items / total_items if total_items else 0

st.progress(progress)

st.write(f"완료 : {checked_items} / {total_items}개")

st.divider()

st.subheader("📝 추가 구매 메모")

memo = st.text_area(
    "필요한 물건을 자유롭게 작성하세요.",
    height=120
)

if st.button("메모 저장"):
    if memo.strip():
        st.success("메모가 저장되었습니다.")
    else:
        st.warning("메모를 입력해주세요.")

st.divider()

st.info(
    """
💡 장보기 팁

• 월~금 : 신선식품 위주 구매

• 토요일 : 간식 및 음료 보충

• 일요일 : 비축용 식품과 생활용품 점검
"""
)
