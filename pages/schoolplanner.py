                import streamlit as st
import pandas as pd
import random
from io import StringIO

st.set_page_config(
    page_title="AI 학교 시간표 생성기",
    page_icon="📚",
    layout="wide"
)

# -------------------------
# 함수
# -------------------------

def generate_timetable(subjects, periods_per_day=7):
    days = ["월", "화", "수", "목", "금"]

    total_slots = periods_per_day * len(days)

    subject_pool = []

    for subject, count in subjects.items():
        subject_pool.extend([subject] * count)

    if len(subject_pool) > total_slots:
        return None, "입력한 총 시수가 주간 가능 시간보다 많습니다."

    while len(subject_pool) < total_slots:
        subject_pool.append("자율")

    major_subjects = ["국어", "수학", "영어", "과학"]
    activity_subjects = ["체육", "음악", "미술"]

    timetable = {day: [""] * periods_per_day for day in days}

    remaining = subject_pool.copy()

    random.shuffle(remaining)

    for day in days:
        for period in range(periods_per_day):

            candidates = remaining.copy()

            if not candidates:
                break

            weighted = []

            for sub in candidates:

                score = 1

                # 오전 선호
                if period < 3 and sub in major_subjects:
                    score += 4

                # 오후 선호
                if period >= 4 and sub in activity_subjects:
                    score += 4

                # 연속 배치 방지
                if period > 0:
                    if timetable[day][period - 1] == sub:
                        score = 0

                weighted.extend([sub] * max(score, 1))

            selected = random.choice(weighted)

            timetable[day][period] = selected
            remaining.remove(selected)

    df = pd.DataFrame(
        timetable,
        index=[f"{i+1}교시" for i in range(periods_per_day)]
    )

    return df, None


# -------------------------
# 제목
# -------------------------

st.title("📚 AI 학교 시간표 자동 생성기")
st.caption("과목별 주당 시수를 입력하면 현실적인 학교 시간표를 자동으로 생성합니다.")

# -------------------------
# 기본 정보
# -------------------------

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox(
        "학년",
        ["1학년", "2학년", "3학년"]
    )

with col2:
    class_name = st.text_input(
        "학급",
        "1반"
    )

with col3:
    periods = st.selectbox(
        "하루 교시 수",
        [5, 6, 7]
    )

st.divider()

# -------------------------
# 과목 입력
# -------------------------

st.subheader("과목 입력")

default_subjects = pd.DataFrame({
    "과목": [
        "국어",
        "수학",
        "영어",
        "과학",
        "사회",
        "체육",
        "음악",
        "미술"
    ],
    "주당시수": [
        5,
        5,
        4,
        3,
        3,
        2,
        1,
        1
    ]
})

edited = st.data_editor(
    default_subjects,
    num_rows="dynamic",
    use_container_width=True
)

# -------------------------
# 생성 버튼
# -------------------------

if st.button("🎯 시간표 생성", use_container_width=True):

    try:

        subjects = {}

        for _, row in edited.iterrows():

            subject = str(row["과목"]).strip()

            if subject == "":
                continue

            count = int(row["주당시수"])

            if count <= 0:
                continue

            subjects[subject] = count

        if len(subjects) == 0:
            st.error("최소 1개 이상의 과목을 입력하세요.")
            st.stop()

        timetable, error = generate_timetable(
            subjects,
            periods
        )

        if error:
            st.error(error)
            st.stop()

        st.success(
            f"{grade} {class_name} 시간표가 생성되었습니다."
        )

        st.subheader("📅 생성된 시간표")

        st.dataframe(
            timetable,
            use_container_width=True
        )

        csv = timetable.to_csv(
            encoding="utf-8-sig"
        )

        st.download_button(
            label="⬇️ CSV 다운로드",
            data=csv,
            file_name=f"{grade}_{class_name}_시간표.csv",
            mime="text/csv"
        )

        st.subheader("📊 과목별 시수 확인")

        count_result = {}

        for subject in subjects:
            count_result[subject] = (
                timetable == subject
            ).sum().sum()

        summary_df = pd.DataFrame({
            "과목": count_result.keys(),
            "배정시수": count_result.values()
        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")

# -------------------------
# 사용 안내
# -------------------------

with st.expander("사용 방법"):
    st.markdown("""
    1. 학년과 학급을 선택합니다.
    2. 과목과 주당 시수를 입력합니다.
    3. 시간표 생성 버튼을 누릅니다.
    4. 자동 생성된 시간표를 확인합니다.
    5. CSV로 다운로드할 수 있습니다.
    """)
