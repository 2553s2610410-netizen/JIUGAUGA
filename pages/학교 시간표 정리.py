import streamlit as st
import pandas as pd

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="학교 시간표 정리",
    page_icon="📚",
    layout="wide"
)

st.title("📚 학교 시간표 정리")
st.caption("학생용 주간 시간표 관리 앱")

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "schedule" not in st.session_state:
    st.session_state.schedule = []

# ---------------------------
# 사이드바
# ---------------------------
with st.sidebar:
    st.header("➕ 수업 추가")

    day = st.selectbox(
        "요일",
        ["월", "화", "수", "목", "금"]
    )

    period = st.selectbox(
        "교시",
        list(range(1, 11))
    )

    subject = st.text_input("과목명")

    classroom = st.text_input("강의실")

    add_btn = st.button("시간표 추가")

    if add_btn:
        try:
            if not subject.strip():
                st.warning("과목명을 입력하세요.")
            else:
                st.session_state.schedule.append({
                    "요일": day,
                    "교시": period,
                    "과목": subject.strip(),
                    "강의실": classroom.strip()
                })
                st.success("추가 완료")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# ---------------------------
# 데이터 표시
# ---------------------------
st.subheader("📝 등록된 수업")

if st.session_state.schedule:

    df = pd.DataFrame(st.session_state.schedule)

    df = df.sort_values(
        by=["요일", "교시"]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # 삭제 기능
    st.subheader("🗑 수업 삭제")

    delete_index = st.selectbox(
        "삭제할 행 선택",
        range(len(df)),
        format_func=lambda x:
        f"{df.iloc[x]['요일']} {df.iloc[x]['교시']}교시 - {df.iloc[x]['과목']}"
    )

    if st.button("선택 삭제"):
        try:
            original = st.session_state.schedule

            target = df.iloc[delete_index].to_dict()

            for i, item in enumerate(original):
                if (
                    item["요일"] == target["요일"]
                    and item["교시"] == target["교시"]
                    and item["과목"] == target["과목"]
                    and item["강의실"] == target["강의실"]
                ):
                    del original[i]
                    break

            st.success("삭제 완료")
            st.rerun()

        except Exception as e:
            st.error(f"삭제 오류: {e}")

    # ---------------------------
    # 시간표 형태 출력
    # ---------------------------
    st.subheader("📅 주간 시간표")

    timetable = pd.DataFrame(
        "",
        index=range(1, 11),
        columns=["월", "화", "수", "목", "금"]
    )

    for _, row in df.iterrows():
        timetable.loc[
            row["교시"],
            row["요일"]
        ] = f"{row['과목']}\n({row['강의실']})"

    st.dataframe(
        timetable,
        use_container_width=True,
        height=420
    )

    # ---------------------------
    # CSV 다운로드
    # ---------------------------
    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name="school_schedule.csv",
        mime="text/csv"
    )

else:
    st.info("등록된 수업이 없습니다.")

# ---------------------------
# 초기화
# ---------------------------
st.divider()

if st.button("전체 시간표 초기화"):
    try:
        st.session_state.schedule = []
        st.success("초기화 완료")
        st.rerun()
    except Exception as e:
        st.error(f"초기화 오류: {e}")
