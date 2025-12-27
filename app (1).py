
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

    # Columns that are NOT marks
    non_mark_columns = ["S.No.", "Class", "Section", "Roll No", "Roll No.", "Student Name"]

    # Columns that contain marks
    subject_columns = [col for col in df.columns if col not in non_mark_columns]

    # Reshape dataframe from wide to long format
    df_long = df.melt(
        id_vars=["Student Name"],
        value_vars=subject_columns,
        var_name="Subject",
        value_name="Marks"
    )

    # Clean student names: strip, uppercase
    df_long["Student Name"] = (
        df_long["Student Name"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Convert marks to numeric and drop rows with missing marks
    df_long["Marks"] = pd.to_numeric(df_long["Marks"], errors="coerce")
    df_long = df_long.dropna(subset=["Marks"])

    # Option selector for user interaction
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

        # Color setup for bars
        colors = cm.get_cmap('tab20').colors
        num_bars = len(student_data["Subject"])
        bar_colors = colors[:num_bars]

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(student_data["Subject"], student_data["Marks"], color=bar_colors)
        ax.set_title(f"{student} - Subject-wise Marks")
        ax.set_ylabel("Marks")
        ax.set_xlabel("Subject")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # OPTION 2: Subject-wise Class Average
    elif option == "Subject-wise Class Average":
        avg_data = df_long.groupby("Subject")["Marks"].mean().reset_index()
        st.dataframe(avg_data)

        # Color setup for bars
        colors = cm.get_cmap('tab20').colors
        num_bars = len(avg_data["Subject"])
        bar_colors = colors[:num_bars]

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(avg_data["Subject"], avg_data["Marks"], color=bar_colors)
        ax.set_title("📘 Subject-wise Class Average")
        ax.set_ylabel("Average Marks")
        ax.set_xlabel("Subject")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # OPTION 3: View Cleaned Data
    else:
        st.dataframe(df_long)
