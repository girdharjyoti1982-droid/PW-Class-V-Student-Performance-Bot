
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

st.set_page_config(page_title="Class V Student Performance Bot")

st.title("🎓 Class V Student Performance Bot")

# Upload Excel file
uploaded_file = st.file_uploader("📂 Upload Class V Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    non_mark_columns = ["S.No.", "Class", "Section", "Roll No", "Roll No.", "Student Name"]
    subject_columns = [col for col in df.columns if col not in non_mark_columns]

    df_long = df.melt(
        id_vars=["Student Name"],
        value_vars=subject_columns,
        var_name="Subject",
        value_name="Marks"
    )

    df_long["Student Name"] = (
        df_long["Student Name"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_long["Marks"] = pd.to_numeric(df_long["Marks"], errors="coerce")
    df_long = df_long.dropna(subset=["Marks"])

    option = st.selectbox(
        "📊 Choose an option",
        ["Student-wise Performance", "Subject-wise Class Average", "View Cleaned Data"]
    )

    # OPTION 1: Student-wise Performance
    if option == "Student-wise Performance":
        student = st.selectbox(
            "👦 Select Student Name",
            sorted(df_long["Student Name"].unique())
        )

        student_data = df_long[df_long["Student Name"] == student]
        st.dataframe(student_data)

        colors = cm.get_cmap('tab20').colors
        num_bars = len(student_data["Subject"])
        bar_colors = colors[:num_bars]

        fig, ax = plt.subplots(figsize=(10, 6)
