import streamlit as st
import pandas as pd
import random
import time
from pathlib import Path
from PIL import Image


@st.cache_data
def load_questions(excel_file: str) -> pd.DataFrame:
    """Load and clean the question bank from the provided Excel file.

    The Excel sheet contains a header row at position 1 and an extra unused column
    that we drop. Column names are normalised for easier access. All questions
    with missing text are removed and the correct answer column is upper‑cased
    for consistency.

    Args:
        excel_file: Path to the Excel file containing the questions.

    Returns:
        A cleaned pandas DataFrame with the following columns:
            index, question, A, B, C, D, E, correct, reference, clause
    """
    df = pd.read_excel(excel_file, sheet_name="Sheet1", header=1)
    # Drop completely empty column if present
    if "Unnamed: 10" in df.columns:
        df = df.drop(columns=["Unnamed: 10"])
    # Rename to more friendly column names
    df = df.rename(
        columns={
            "TT": "index",
            "Câu hỏi": "question",
            "Phương án A": "A",
            "Phương án B": "B",
            "Phương án C": "C",
            "Phương án D": "D",
            "Phương án E": "E",
            "Đ.án đúng": "correct",
            "Số văn bản tham chiếu (kèm trích yếu văn bản)": "reference",
            "Điều khoản tham chiếu cụ thể": "clause",
        }
    )
    # Remove questions without text
    df = df[df["question"].notna()].reset_index(drop=True)
    # Normalise correct answer
    df["correct"] = df["correct"].astype(str).str.strip().str.upper()
    return df


def initialise_session():
    """Initialise Streamlit session state variables used in the app."""
    state_defaults = {
        "quiz_started": False,
        "quiz_ended": False,
        "num_questions": 0,
        "questions": None,
        "current_q": 0,
        "answers": [],
        "start_time": None,
    }
    for key, value in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_quiz(df: pd.DataFrame, num_questions: int):
    """Prepare the quiz by sampling questions and resetting session variables."""
    st.session_state.quiz_started = True
    st.session_state.quiz_ended = False
    st.session_state.num_questions = num_questions
    # Randomly sample without replacement
    sampled = df.sample(num_questions, replace=False).reset_index(drop=True)
    st.session_state.questions = sampled
    st.session_state.current_q = 0
    st.session_state.answers = [None] * num_questions
    st.session_state.start_time = time.time()


def render_header():
    """Render the hero section at the top of the app."""
    # Load hero image
    header_path = Path(__file__).parent / "assets" / "app_header.png"
    if header_path.exists():
        header_img = Image.open(header_path)
        st.image(header_img, use_column_width=True)
    # Title and tagline
    st.markdown(
        """
        <div style="text-align: center; margin-top: -1rem;">
            <h1 style="color:#6C3DA8; font-size: 3rem; margin-bottom:0.2rem;">Ôn tập NLCM</h1>
            <p style="font-size:1.25rem; color:#444;">Cùng luyện tập và cải thiện kỹ năng của bạn với bộ câu hỏi chuẩn bị sẵn!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timer(total_seconds: int = 3600):
    """Display the remaining time in the sidebar. Ends quiz when time runs out."""
    elapsed = time.time() - st.session_state.start_time
    remaining = total_seconds - elapsed
    if remaining <= 0:
        st.session_state.quiz_ended = True
        remaining = 0
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    st.sidebar.markdown(
        f"<h3 style='color:#6C3DA8;'>Thời gian còn lại</h3><p style='font-size:24px;'>{minutes:02d}:{seconds:02d}</p>",
        unsafe_allow_html=True,
    )


def render_question():
    """Render the current question with answer options and navigation buttons."""
    idx = st.session_state.current_q
    total = st.session_state.num_questions
    question_row = st.session_state.questions.iloc[idx]
    st.markdown(f"### Câu {idx+1} / {total}")
    st.write(question_row["question"])
    # Build list of (option_key, option_text)
    options = []
    for opt_key in ["A", "B", "C", "D", "E"]:
        opt_text = question_row.get(opt_key)
        if pd.notna(opt_text):
            options.append((opt_key, opt_text))
    # Map to labels and values for radio button
    option_keys = [opt_key for opt_key, _ in options]
    # Retrieve previous answer if exists to preselect
    preselect = None
    prev_answer = st.session_state.answers[idx]
    if prev_answer in option_keys:
        preselect = option_keys.index(prev_answer)
    # Render radio buttons
    def format_label(k):
        # Find corresponding text
        for key, text in options:
            if key == k:
                return f"{key}. {text}"
        return k

    choice = st.radio(
        "Chọn đáp án:",
        option_keys,
        index=preselect if preselect is not None else 0,
        format_func=format_label,
        key=f"radio_{idx}"
    )
    st.session_state.answers[idx] = choice
    # Navigation buttons
    col_prev, col_next = st.columns([1, 1])
    if col_prev.button("⬅ Quay lại", disabled=(idx == 0)):
        st.session_state.current_q -= 1
        st.experimental_rerun()
    if idx < total - 1:
        if col_next.button("Tiếp theo ➡"):
            st.session_state.current_q += 1
            st.experimental_rerun()
    else:
        if col_next.button("Nộp bài ✅"):
            st.session_state.quiz_ended = True
            st.experimental_rerun()


def render_results():
    """Calculate and display quiz results."""
    df = st.session_state.questions
    total = st.session_state.num_questions
    user_answers = st.session_state.answers
    # Compute correct answers
    correct_list = []
    for i in range(total):
        row = df.iloc[i]
        correct_key = row["correct"]
        user_key = user_answers[i]
        is_correct = str(user_key).strip().upper() == str(correct_key).strip().upper()
        correct_list.append(is_correct)
    num_correct = sum(correct_list)
    score_percent = (num_correct / total) * 100
    # Show summary
    st.markdown(
        f"<h2 style='color:#6C3DA8;'>Kết quả của bạn</h2>", unsafe_allow_html=True
    )
    st.write(f"Số câu đúng: {num_correct}/{total}")
    st.write(f"Điểm số: {score_percent:.1f}%")
    # Detailed table
    st.markdown("#### Chi tiết các câu hỏi")
    result_data = []
    for i in range(total):
        row = df.iloc[i]
        result_data.append({
            "#": i + 1,
            "Câu hỏi": row["question"],
            "Đáp án của bạn": user_answers[i],
            "Đáp án đúng": row["correct"],
            "Kết quả": "✔️" if correct_list[i] else "❌",
        })
    result_df = pd.DataFrame(result_data)
    st.dataframe(result_df, use_container_width=True)
    # Restart button
    if st.button("Làm lại bài thi 🔄"):
        # Reset state
        for key in ["quiz_started", "quiz_ended", "num_questions", "questions", "current_q", "answers", "start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()


def main():
    st.set_page_config(
        page_title="Ôn tập NLCM Quiz",
        page_icon="🎓",
        layout="wide",
    )
    initialise_session()
    df = load_questions(str(Path(__file__).parent / "Cau hoi on tap 2025.xlsx"))
    render_header()
    # If quiz not started or ended, show setup panel
    if not st.session_state.quiz_started:
        st.markdown("## Chọn số câu hỏi để bắt đầu ôn tập")
        num = st.selectbox("Số câu hỏi", [10, 20, 50], index=0)
        st.write("Bạn có 60 phút để hoàn thành bài.")
        if st.button("Bắt đầu ôn tập 🚀"):
            start_quiz(df, num)
            st.experimental_rerun()
    else:
        # Timer and quiz in progress or ended
        render_timer(total_seconds=3600)  # 60 minutes
        if st.session_state.quiz_ended:
            render_results()
        else:
            render_question()


if __name__ == "__main__":
    main()