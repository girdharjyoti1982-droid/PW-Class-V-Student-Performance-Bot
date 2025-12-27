
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    # OPTION 1
    if option == "Student-wise Performance":
        student = st.selectbox(
            "👦 Select Student Name",
            sorted(df_long["Student Name"].unique())
        )

        student_data = df_long[df_long["Student Name"] == student]
        st.dataframe(student_data)

        fig, ax = plt.subplots()
        ax.bar(student_data["Subject"], student_data["Marks"])
        ax.set_title(f"{student} - Subject-wise Marks")
        ax.set_ylabel("Marks")
        ax.set_xlabel("Subject")
        st.pyplot(fig)

    # OPTION 2
    elif option == "Subject-wise Class Average":
        avg_data = df_long.groupby("Subject")["Marks"].mean().reset_index()
        st.dataframe(avg_data)

        fig, ax = plt.subplots()
        ax.bar(avg_data["Subject"], avg_data["Marks"])
        ax.set_title("📘 Subject-wise Class Average")
        st.pyplot(fig)

    # OPTION 3
    else:
        st.dataframe(df_long)

