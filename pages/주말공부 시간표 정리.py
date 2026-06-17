import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="주말 공부 시간표 정리",
    page_icon="📚",
    layout="wide"
)

st.title("📚 주말 공부 시간표 정리")
st.caption("토요일과 일요일 공부 계획을 쉽고 체계적으로 관리해보세요.")

# 세션 상태 초기화
if "schedule" not in st.session_state:
    st.session_state.schedule = []

# 사이드바
st.sidebar.header("➕ 공부 계획 추가")

subject = st.sidebar.text_input("과목명")
day = st.sidebar.selectbox("요일", ["토요일", "일요일"])
start_time = st.sidebar.time_input("시작 시간")
end_time = st.sidebar.time_input("종료 시간")
priority = st.sidebar.selectbox(
    "우선순위",
    ["높음", "보통", "낮음"]
)

add_btn = st.sidebar.button("추가하기")

if add_btn:
    try:
        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute

        if not subject.strip():
            st.sidebar.error("과목명을 입력하세요.")
        elif end_minutes <= start_minutes:
            st.sidebar.error("종료 시간은 시작 시간보다 늦어야 합니다.")
        else:
            duration = (end_minutes - start_minutes) / 60

            st.session_state.schedule.append({
                "요일": day,
                "과목": subject.strip(),
                "시작": start_time.strftime("%H:%M"),
                "종료": end_time.strftime("%H:%M"),
                "공부시간(시간)": round(duration, 1),
                "우선순위": priority
            })

            st.sidebar.success("추가 완료!")

    except Exception:
        st.sidebar.error("일정 추가 중 오류가 발생했습니다.")

# 데이터프레임 생성
df = pd.DataFrame(st.session_state.schedule)

# 통계 영역
st.subheader("📊 주말 공부 현황")

if not df.empty:
    total_hours = df["공부시간(시간)"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("총 공부 시간", f"{total_hours:.1f}시간")
    col2.metric("계획 수", len(df))
    col3.metric("과목 수", df["과목"].nunique())

else:
    st.info("아직 등록된 공부 계획이 없습니다.")

# 시간표 표시
st.subheader("🗓️ 시간표")

if not df.empty:

    saturday_df = df[df["요일"] == "토요일"]
    sunday_df = df[df["요일"] == "일요일"]

    tab1, tab2 = st.tabs(["토요일", "일요일"])

    with tab1:
        if not saturday_df.empty:
            st.dataframe(
                saturday_df,
                use_container_width=True
            )
        else:
            st.write("등록된 일정이 없습니다.")

    with tab2:
        if not sunday_df.empty:
            st.dataframe(
                sunday_df,
                use_container_width=True
            )
        else:
            st.write("등록된 일정이 없습니다.")

# 과목별 공부 시간
st.subheader("📈 과목별 공부 시간")

if not df.empty:
    subject_summary = (
        df.groupby("과목")["공부시간(시간)"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(subject_summary)

# 삭제 기능
st.subheader("🗑️ 일정 삭제")

if not df.empty:

    delete_index = st.selectbox(
        "삭제할 일정 선택",
        range(len(df)),
        format_func=lambda x:
        f"{df.iloc[x]['요일']} | {df.iloc[x]['과목']} | {df.iloc[x]['시작']}~{df.iloc[x]['종료']}"
    )

    if st.button("선택 일정 삭제"):
        try:
            st.session_state.schedule.pop(delete_index)
            st.success("삭제되었습니다.")
            st.rerun()
        except Exception:
            st.error("삭제 중 오류가 발생했습니다.")

# 다운로드
st.subheader("💾 저장")

if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name="weekend_study_schedule.csv",
        mime="text/csv"
    )

# 공부 팁
st.subheader("🎯 추천 공부 전략")

st.markdown("""
- 우선순위가 높은 과목을 오전에 배치하기
- 50분 공부 + 10분 휴식
- 어려운 과목 → 쉬운 과목 순서로 구성
- 일요일 저녁에는 복습 시간 확보
- 총 공부 시간을 무리하게 늘리기보다 꾸준히 유지하기
""")
