
import streamlit as st
import pandas as pd
import plotly.express as px

from ml.predict import predict_account

st.set_page_config(
    page_title="Fake Account Detection",
    page_icon="🛡️",
    layout="wide"
)

FEATURES = [
    "profile pic",
    "nums/length username",
    "fullname words",
    "nums/length fullname",
    "name==username",
    "description length",
    "external URL",
    "private",
    "#posts",
    "#followers",
    "#follows"
]

st.title("🛡️ Fake Social Media Account Detection")
st.caption("AI-powered moderator review and account risk analysis")

st.sidebar.title("Moderator Panel")
st.sidebar.success("System Online")
st.sidebar.write("Model: Random Forest")
st.sidebar.write("Dataset: Instagram profiles")

tab1, tab2 = st.tabs([
    "Individual Account Analysis",
    "Moderator Review Dashboard"
])

# -----------------------------------
# TAB 1: INDIVIDUAL ACCOUNT ANALYSIS
# -----------------------------------

with tab1:

    st.header("Account Profile Analysis")
    st.write("Enter the available profile details.")

    with st.form("account_form"):

        col1, col2 = st.columns(2)

        with col1:
            profile_pic = st.selectbox(
                "Profile Picture Available?",
                ["Yes", "No"]
            )

            username_ratio = st.number_input(
                "Numbers / Length of Username",
                0.0, 1.0, 0.2
            )

            fullname_words = st.number_input(
                "Full Name Words", min_value=0, value=2
            )

            fullname_ratio = st.number_input(
                "Numbers / Length of Full Name",
                0.0, 1.0, 0.0
            )

            name_match = st.selectbox(
                "Name Same as Username?", ["No", "Yes"]
            )

            description_length = st.number_input(
                "Description Length", min_value=0, value=50
            )

        with col2:
            external_url = st.selectbox(
                "External URL Available?", ["No", "Yes"]
            )

            private = st.selectbox(
                "Private Account?", ["No", "Yes"]
            )

            posts = st.number_input(
                "Number of Posts", min_value=0, value=20
            )

            followers = st.number_input(
                "Number of Followers", min_value=0, value=500
            )

            follows = st.number_input(
                "Number of Following", min_value=0, value=300
            )

        analyse = st.form_submit_button(
            "Analyse Account",
            use_container_width=True
        )

    if analyse:

        account = {
            "profile pic": 1 if profile_pic == "Yes" else 0,
            "nums/length username": username_ratio,
            "fullname words": fullname_words,
            "nums/length fullname": fullname_ratio,
            "name==username": 1 if name_match == "Yes" else 0,
            "description length": description_length,
            "external URL": 1 if external_url == "Yes" else 0,
            "private": 1 if private == "Yes" else 0,
            "#posts": posts,
            "#followers": followers,
            "#follows": follows
        }

        result = predict_account(account)

        st.subheader("Analysis Results")

        c1, c2, c3 = st.columns(3)

        c1.metric("Prediction", result["prediction"])
        c2.metric("Risk Score", f'{result["risk_score"]}%')
        c3.metric("Risk Level", result["risk_level"])

        st.progress(int(result["risk_score"]))

        st.subheader("Warning Indicators")

        if result["indicators"]:
            for indicator in result["indicators"]:
                st.warning(indicator)
        else:
            st.success("No predefined warning indicators detected.")

        st.info(
            "The score is a model estimate, not proof of fake activity. "
            "A moderator should review the available evidence."
        )


# -----------------------------------
# TAB 2: MODERATOR REVIEW DASHBOARD
# -----------------------------------

with tab2:

    st.header("Moderator Review Dashboard")

    st.write(
        "Upload a CSV file containing multiple account profiles "
        "to analyse them together."
    )

    st.info(
        "The uploaded CSV must contain all 11 model feature columns. "
        "Optional columns: account_id and username."
    )

    uploaded_file = st.file_uploader(
        "Upload Account Dataset (CSV)",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            missing = [
                col for col in FEATURES if col not in df.columns
            ]

            if missing:
                st.error(
                    "Missing required columns: "
                    + ", ".join(missing)
                )

            elif df.empty:
                st.warning("The uploaded CSV contains no accounts.")

            else:
                if len(df) > 1000:
                    st.warning(
                        "For this demo, only the first 1000 rows "
                        "will be analysed."
                    )
                    df = df.head(1000).copy()

                st.write("Uploaded profiles:", len(df))

                if st.button(
                    "Analyse All Accounts",
                    type="primary"
                ):

                    results = []

                    progress = st.progress(0)
                    status = st.empty()

                    for index, (_, row) in enumerate(df.iterrows()):

                        account = {
                            feature: row[feature]
                            for feature in FEATURES
                        }

                        prediction = predict_account(account)

                        results.append({
                            "Account ID": row.get(
                                "account_id",
                                f"Account_{index + 1}"
                            ),
                            "Username": row.get(
                                "username",
                                f"Profile_{index + 1}"
                            ),
                            "Prediction": prediction["prediction"],
                            "Risk Score": prediction["risk_score"],
                            "Risk Level": prediction["risk_level"],
                            "Warning Indicators": "; ".join(
                                prediction["indicators"]
                            )
                        })

                        progress.progress(
                            (index + 1) / len(df)
                        )

                        status.text(
                            f"Analysing account {index + 1} "
                            f"of {len(df)}"
                        )

                    result_df = pd.DataFrame(results)

                    st.session_state["review_results"] = result_df

                    status.success("Account analysis completed!")

        except Exception as error:
            st.error(f"Unable to analyse dataset: {error}")

    # Display moderator results
    if "review_results" in st.session_state:

        result_df = st.session_state["review_results"]

        st.divider()
        st.subheader("Account Statistics")

        total = len(result_df)

        suspicious = (
            result_df["Prediction"] == "Suspicious"
        ).sum()

        genuine = (
            result_df["Prediction"] == "Genuine"
        ).sum()

        high_risk = (
            result_df["Risk Level"] == "High"
        ).sum()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Accounts", total)
        c2.metric("Suspicious Accounts", int(suspicious))
        c3.metric("Genuine Accounts", int(genuine))
        c4.metric("High Risk Accounts", int(high_risk))

        st.divider()

        # Risk distribution chart
        st.subheader("Risk Distribution")

        risk_counts = (
            result_df["Risk Level"]
            .value_counts()
            .reindex(["Low", "Medium", "High"], fill_value=0)
            .rename_axis("Risk Level")
            .reset_index(name="Accounts")
        )

        fig = px.bar(
            risk_counts,
            x="Risk Level",
            y="Accounts",
            color="Risk Level",
            title="Account Risk Distribution",
            color_discrete_map={
                "Low": "#2EAD65",
                "Medium": "#E5A000",
                "High": "#E05252"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        # Moderator review queue
        st.divider()
        st.subheader("⚠️ Moderator Review Queue")

        review_df = result_df[
            result_df["Prediction"] == "Suspicious"
        ].sort_values(
            "Risk Score",
            ascending=False
        )

        if not review_df.empty:

            st.write(
                "These accounts are flagged for human review."
            )

            st.dataframe(
                review_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.success("No accounts were flagged as suspicious.")

        # Full results
        st.divider()
        st.subheader("All Analysed Accounts")

        st.dataframe(
            result_df.sort_values(
                "Risk Score",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        # Download report
        csv_data = result_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Moderator Report",
            data=csv_data,
            file_name="moderator_review_report.csv",
            mime="text/csv"
        )

        st.info(
            "Risk scores are model estimates. Flagged accounts "
            "must be reviewed by a human moderator before any action."
        )

st.divider()

st.caption(
    "Fake Social Media Account Detection System | Hackathon Project"
)
