```python
import streamlit as st
from datetime import datetime

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="마트 장보기 플래너",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background-color: #f6f8fc;
}

.main-header {
    background: linear-gradient(135deg, #4CAF50, #81C784);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.tip-box {
    background: #e8f5e9;
    border-left: 6px solid #4CAF50;
    padding: 15px;
    border-radius: 10px;
}

div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #43A047;
}

.stProgress > div > div > div > div {
    background-color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터
# -----------------------------
shopping_data = {
    "월요일": {
        "🥛 신선식품": ["우유", "계란", "두부"],
        "🥬 채소": ["상추", "양파", "대파"]
    },
    "화요일": {
        "🥛 신선식품": ["요거트", "치즈"],
        "🥕 채소": ["오이", "당근"]
    },
    "수요일": {
        "🍗 단백질": ["닭가슴살", "햄"],
        "🥦 채소": ["브로콜리", "파프리카"]
    },
    "목요일": {
        "🥛 유제품": ["두유", "버터"],
        "🥔 채소": ["감자", "양배추"]
    },
    "금요일": {
        "🥩 육류": ["소고기", "돼지고기"],
        "🍄 채소": ["버섯", "깻잎"]
    },
    "토요일": {
        "🍪 간식": ["과자", "아이스크림"],
        "🥤 음료": ["주스", "탄산음료"]
    },
    "일요일": {
        "🍜 비축식품": ["라면", "즉석밥"],
        "🧻 생활용품": ["휴지", "세제"]
    }
}

# -----------------------------
# 헤더
# -----------------------------
st.markdown("""
<div class="main-header">
    <h1>🛒 마트 장보기 플래너</h1>
    <p>요일별 추천 장보기 목록을 확인하고 체크해보세요</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 이미지
# -----------------------------
st.image(
    "https://images.unsplash.com/photo-1542838132-92c53300491e",
    use_container_width=True
)

# -----------------------------
# 오늘 요일
# -----------------------------
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
    "📅 장보는 요일 선택",
    list(shopping_data.keys()),
    index=list(shopping_data.keys()).index(today)
)

st.markdown(
    f"<div class='card'><h3>{selected_day} 추천 장보기 목록</h3></div>",
    unsafe_allow_html=True
)

total_items = 0
checked_items = 0

for category, items in shopping_data[selected_day].items():

    st.markdown(
        f"<div class='card'><h4>{category}</h4></div>",
        unsafe_allow_html=True
    )

    for item in items:
        total_items += 1

        if st.checkbox(item, key=f"{selected_day}_{item}"):
            checked_items += 1

# -----------------------------
# 진행률
# -----------------------------
progress = checked_items / total_items if total_items else 0

st.subheader("📊 진행 상황")

st.progress(progress)

st.metric(
    "구매 완료",
    f"{checked_items}/{total_items}"
)

# -----------------------------
# 메모
# -----------------------------
st.subheader("📝 추가 구매 목록")

memo = st.text_area(
    "추가로 구매할 물건을 입력하세요",
    height=120
)

if st.button("저장하기"):
    if memo.strip():
        st.success("메모가 저장되었습니다.")
    else:
        st.warning("내용을 입력해주세요.")

# -----------------------------
# 팁
# -----------------------------
st.markdown("""
<div class="tip-box">
<h4>💡 장보기 팁</h4>
<ul>
<li>월~금 : 신선식품 중심</li>
<li>토요일 : 간식 및 음료 보충</li>
<li>일요일 : 생활용품 재고 확인</li>
</ul>
</div>
""", unsafe_allow_html=True)
```
