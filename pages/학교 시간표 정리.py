import streamlit as st
import pandas as pd

# ------------------------
# 페이지 설정
# ------------------------
st.set_page_config(
    page_title="학교 시간표",
    page_icon="📚",
    layout="wide"
)

# ------------------------
# CSS
# ------------------------
st.markdown("""
<style>

.main {
    background-color: #f6f8fc;
}

.hero {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.hero h1{
    margin-bottom:0;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.small-title{
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
}

.stButton > button{
    width:100%;
    border:none;
    border-radius:10px;
    background:#4f46e5;
    color:white;
    font-weight:bold;
}

.stButton > button:hover{
    background:#4338ca;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# 헤더
# ------------------------
st.markdown("""
<div class="hero">
    <h1>📚 학교 시간표 관리</h1>
    <p>주간 수업을 쉽고 깔끔하게 관리하세요</p>
</div>
""", unsafe_allow_html=True)

# ------------------------
# 세션 상태
# ------------------------
if "schedule" not in st.session_state:
    st.session_state.schedule = []

# ------------------------
# 색상
# ------------------------
subject_colors = [
    "#dbeafe",
    "#dcfce7",
    "#fef3c7",
    "#fce7f3",
    "#ede9fe",
    "#cffafe",
    "#fde68a",
    "#fecaca"
]

# ------------------------
# 좌우 레이아웃
# ------------------------
left, right = st.columns([1, 2])

# ------------------------
# 입력 영역
# ------------------------
with left:

    st.markdown(
        '<div class="card"><div class="small-title">➕ 수업 추가</div>',
        unsafe_allow_html=True
    )

    day = st.selectbox(
        "요일",
        ["월", "화", "수", "목", "금"]
    )

    period = st.selectbox(
        "교시",
        range(1, 11)
    )

    subject = st.text_input("과목명")

    classroom = st.text_input("강의실")

    if st.button("추가하기"):
        try:
            if subject.strip() == "":
                st.warning("과목명을 입력하세요.")
            else:
                st.session_state.schedule.append({
                    "요일": day,
                    "교시": period,
                    "과목": subject.strip(),
                    "강의실": classroom.strip()
                })
                st.success("추가 완료")
                st.rerun()

        except Exception as e:
            st.error(f"오류: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------
# 시간표
# ------------------------
with right:

    st.markdown(
        '<div class="card"><div class="small-title">📅 주간 시간표</div>',
        unsafe_allow_html=True
    )

    if st.session_state.schedule:

        df = pd.DataFrame(st.session_state.schedule)

        timetable = pd.DataFrame(
            "",
            index=range(1, 11),
            columns=["월", "화", "수", "목", "금"]
        )

        color_map = {}

        subjects = df["과목"].unique()

        for i, sub in enumerate(subjects):
            color_map[sub] = subject_colors[
                i % len(subject_colors)
            ]

        for _, row in df.iterrows():
            timetable.loc[
                row["교시"],
                row["요일"]
            ] = f"{row['과목']}<br><small>{row['강의실']}</small>"

        html = """
        <table style="
            width:100%;
            border-collapse:collapse;
            text-align:center;
        ">
        <tr style="
            background:#4f46e5;
            color:white;
        ">
        <th>교시</th>
        <th>월</th>
        <th>화</th>
        <th>수</th>
        <th>목</th>
        <th>금</th>
        </tr>
        """

        for period_num in timetable.index:

            html += f"<tr><td><b>{period_num}</b></td>"

            for day_name in timetable.columns:

                value = timetable.loc[
                    period_num,
                    day_name
                ]

                bg = "#ffffff"

                if value:

                    sub_name = value.split("<br>")[0]

                    bg = color_map.get(
                        sub_name,
                        "#f3f4f6"
                    )

                html += f"""
                <td style="
                    border:1px solid #e5e7eb;
                    padding:10px;
                    background:{bg};
                    border-radius:8px;
                ">
                {value}
                </td>
                """

            html += "</tr>"

        html += "</table>"

        st.markdown(
            html,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.subheader("📋 수업 목록")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 CSV 다운로드",
            csv,
            "schedule.csv",
            "text/csv"
        )

        idx = st.selectbox(
            "삭제할 수업",
            range(len(df)),
            format_func=lambda x:
            f"{df.iloc[x]['요일']} "
            f"{df.iloc[x]['교시']}교시 - "
            f"{df.iloc[x]['과목']}"
        )

        if st.button("🗑 선택 삭제"):
            del st.session_state.schedule[idx]
            st.rerun()

        if st.button("🚨 전체 초기화"):
            st.session_state.schedule = []
            st.rerun()

    else:
        st.info("등록된 수업이 없습니다.")

    st.markdown("</div>", unsafe_allow_html=True)
