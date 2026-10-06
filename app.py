import streamlit as st

from resume_analyzer import (
    extract_text,
    calculate_similarity,
    store_resume
)

from job_data import JOBS


st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -------------------------------
# TITLE
# -------------------------------

st.title("📄 Intelligent Resume Analyzer")
st.subheader("AI-Powered Resume and Job Matching System")

st.write(
    "Upload your resume and discover the jobs that best match your profile."
)


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("Navigation")

st.sidebar.info(
    """
    System Features:

    • Resume Upload
    • Resume Text Extraction
    • AI Semantic Matching
    • Job Recommendations
    • Match Score
    • ChromaDB Storage
    """
)


# -------------------------------
# RESUME UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    # -------------------------------
    # ANALYZE BUTTON
    # -------------------------------

    if st.button("🔍 Analyze Resume"):

        with st.spinner(
            "Analyzing your resume using AI..."
        ):

            # Extract resume text
            resume_text = extract_text(
                uploaded_file
            )


            if not resume_text.strip():

                st.error(
                    "Unable to extract text from this PDF."
                )

                st.stop()


            # Store resume
            store_resume(resume_text)


            st.success(
                "Resume analyzed successfully!"
            )


            # -------------------------------
            # RESUME PREVIEW
            # -------------------------------

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text_area(
                    "Resume Content",
                    resume_text,
                    height=300
                )


            # -------------------------------
            # JOB MATCHING
            # -------------------------------

            st.header(
                "🎯 Recommended Jobs"
            )


            results = []


            for job in JOBS:

                score = calculate_similarity(
                    resume_text,
                    job["description"]
                )


                results.append({
                    "title": job["title"],
                    "company": job["company"],
                    "description": job["description"],
                    "score": score
                })


            # Sort jobs by score
            results.sort(
                key=lambda x: x["score"],
                reverse=True
            )


            # -------------------------------
            # DISPLAY RESULTS
            # -------------------------------

            for job in results:

                score = job["score"]


                if score >= 80:

                    status = "🟢 Excellent Match"

                elif score >= 60:

                    status = "🟡 Good Match"

                elif score >= 40:

                    status = "🟠 Partial Match"

                else:

                    status = "🔴 Low Match"


                with st.container():

                    st.subheader(
                        job["title"]
                    )

                    st.write(
                        f"**Company:** {job['company']}"
                    )

                    st.progress(
                        int(score)
                    )

                    st.write(
                        f"**Match Score: {score}%**"
                    )

                    st.write(
                        status
                    )

                    with st.expander(
                        "View Job Description"
                    ):

                        st.write(
                            job["description"]
                        )

                    st.divider()