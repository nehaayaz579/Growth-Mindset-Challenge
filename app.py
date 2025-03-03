import streamlit as st
import pandas as pd
import os
from io import BytesIO
import random

# Setup Our App
st.set_page_config(page_title="Growth Mindset Data Sweeper", layout='wide')
st.title("🧹⭕ Growth Mindset Data Sweeper")
st.write("""
Transform your files between CSV and Excel formats with built-in data cleaning, visualization, and growth mindset-driven features.
""")

# Adding a Growth Mindset Quote
quotes = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "It’s not that I’m so smart, it’s just that I stay with problems longer.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "A person who never made a mistake never tried anything new."
]
quote = random.choice(quotes)
st.write(f"**Motivational Quote**: {quote}")

# Upload files section
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        # File ka info dikhana
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")
        
        # Dataframe ke 5 rows dikhana
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Growth Mindset Challenge: Set Learning Goals
        st.subheader("Growth Mindset Challenge: Set Your Learning Goals")
        goal = st.text_input("What do you want to achieve with this data? Set your goal here.", placeholder="e.g., Clean the data, Analyze trends")
        if goal:
            st.session_state.goal = goal
            st.success(f"Your learning goal is set: {goal}")
        
        # Display Current Goal
        if 'goal' in st.session_state:
            st.write(f"**Your Current Learning Goal**: {st.session_state.goal}")
        
        # Data cleaning ka option
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed! Keep pushing forward!")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been filled! Keep growing!")

        # Choose Specific columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Add Progress Tracker for Growth
        st.subheader("Track Your Progress")
        progress = st.slider("Track your data-cleaning progress (0% to 100%)", 0, 100, 0)
        st.progress(progress)
        
        # Reflection Section
        st.subheader("Reflect on Your Learning")
        reflection = st.text_area("What challenges did you face while cleaning the data? How did you overcome them?", height=150)

        if reflection:
            st.session_state.reflection = reflection
            st.write("**Your Reflection**: ")
            st.write(reflection)

        # Create some visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the files -> csv to excel
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("All Files Processed! Keep growing and learning!")
