from __future__ import annotations

import csv
import io
import os
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LAB_DATA_FILE = DATA_DIR / "qq-users.csv"
ADMIN_PASSWORD = "C1sco123!"

LAB_GUIDE_URL = "https://cloudlabs.apstra.com/labguide/Cloudlabs/6.1.0/"
DCA_SIGNUP_URL = "https://get-dca.osiodyssey.com/"
APSTRA_UI_URL = "https://g-6-1-1-70.t3aco.fragmentationneeded.net/#/login"
DCA_LOGIN_URL = "https://dc.ai.juniper.net//signin.html#!signin"

RESOURCE_LINKS = [
    {
        "title": "Apstra Web UI",
        "description": "Open the Apstra web interface directly for the active lab environment.",
        "url": APSTRA_UI_URL,
    },
    {
        "title": "Lab Guide",
        "description": "Open the current walkthrough lab material.",
        "url": LAB_GUIDE_URL,
    },
    {
        "title": "Data Center Assurance Sign Up",
        "description": "Open the DCA access page for new users and lab participants.",
        "url": DCA_SIGNUP_URL,
    },
    {
        "title": "Data Center Assurance Login",
        "description": "Open the DCA login page for existing users.",
        "url": DCA_LOGIN_URL,
    },
]


def ensure_lab_data_file() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not LAB_DATA_FILE.exists():
        LAB_DATA_FILE.write_text(
            "username,first_name,last_name,password,blueprint_name\n",
            encoding="utf-8",
        )


@st.cache_data(show_spinner=False)
def load_lab_rows() -> list[dict[str, str]]:
    ensure_lab_data_file()
    with LAB_DATA_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def build_display_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return rows


def validate_uploaded_csv(file_bytes: bytes) -> str:
    text = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("The CSV file must include a header row.")

    rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("The CSV file must include at least one data row.")

    return text


def save_uploaded_csv(csv_text: str) -> None:
    ensure_lab_data_file()
    LAB_DATA_FILE.write_text(csv_text, encoding="utf-8")
    load_lab_rows.clear()


def render_link_cards() -> None:
    st.subheader("Resources")
    st.caption("Update the URL constants at the top of this file to change the published links.")

    for first_index in range(0, len(RESOURCE_LINKS), 2):
        columns = st.columns(2, gap="large")
        for column, link in zip(columns, RESOURCE_LINKS[first_index:first_index + 2]):
            with column:
                st.markdown(
                    f"""
                    <div class=\"resource-card\">
                        <p class=\"resource-kicker\">Published Link</p>
                        <h3>{link['title']}</h3>
                        <p>{link['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button(f"Open {link['title']}", link["url"], use_container_width=True, type="primary")


def render_admin_panel() -> None:
    st.divider()
    footer_columns = st.columns([2, 1])
    with footer_columns[1]:
        toggle_label = "Hide Admin Panel" if st.session_state.get("show_admin_panel") else "Admin: Update Lab Details"
        if st.button(toggle_label, use_container_width=True, type="secondary"):
            st.session_state["show_admin_panel"] = not st.session_state.get("show_admin_panel", False)

    if not st.session_state.get("show_admin_panel"):
        return

    st.markdown(
        """
        <div class="admin-panel">
            <p class="admin-kicker">Admin Upload</p>
            <h3>Replace the lab table CSV</h3>
            <p>
                This is intentionally basic password protection. Change <strong>ADMIN_PASSWORD</strong>
                near the top of this file if you want to use a different upload password.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("lab_upload_form", clear_on_submit=True):
        input_columns = st.columns([1, 2], gap="large")
        with input_columns[0]:
            password = st.text_input("Admin Password", type="password", placeholder="Enter password")
        with input_columns[1]:
            uploaded_file = st.file_uploader("Upload replacement CSV", type=["csv"], help="UTF-8 CSV with a header row")
        submit_upload = st.form_submit_button("Replace Lab Table", use_container_width=True)

    if not submit_upload:
        return

    if password != ADMIN_PASSWORD:
        st.error("Incorrect password.")
        return

    if uploaded_file is None:
        st.error("Choose a CSV file to upload.")
        return

    try:
        csv_text = validate_uploaded_csv(uploaded_file.getvalue())
        save_uploaded_csv(csv_text)
    except UnicodeDecodeError:
        st.error("The CSV file must be UTF-8 encoded.")
        return
    except ValueError as exc:
        st.error(str(exc))
        return

    st.success("Lab details updated successfully.")
    st.rerun()


st.set_page_config(
    page_title="Apstra Lab Hub",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                linear-gradient(180deg, #f5f8f7 0%, #eef4f6 100%);
        }

        html, body, [class*="css"]  {
            font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
            color: #0f172a;
        }

        h1, h2, h3 {
            font-family: "Trebuchet MS", "Avenir Next Condensed", sans-serif;
            letter-spacing: -0.03em;
            color: #0f172a;
        }

        p, li, label, .stCaption {
            color: #334155;
        }

        .stMarkdown, .stText, .stCaption, .st-emotion-cache-10trblm, .st-emotion-cache-16txtl3 {
            color: #0f172a;
        }

        [data-testid="stHeadingWithActionElements"] h1,
        [data-testid="stHeadingWithActionElements"] h2,
        [data-testid="stHeadingWithActionElements"] h3,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: #0f172a;
        }

        .hero-shell {
            padding: 1.25rem 1.5rem;
            margin: 0.35rem 0 1.2rem 0;
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.96);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        }

        .hero-kicker {
            margin: 0;
            color: #0f766e;
            text-transform: uppercase;
            font-size: 0.76rem;
            letter-spacing: 0.16em;
            font-weight: 700;
        }

        .hero-copy {
            margin: 0.7rem 0 0 0;
            color: #334155;
            max-width: 52rem;
            font-size: 0.98rem;
            line-height: 1.5;
        }

        .hero-shell h1 {
            color: #0f172a;
            margin: 0.3rem 0 0 0;
        }

        .resource-card {
            padding: 1rem 1rem 0.6rem 1rem;
            min-height: 155px;
            border-radius: 16px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(255, 255, 255, 0.96);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
        }

        .resource-card h3 {
            margin: 0.2rem 0 0.6rem 0;
            color: #0f172a;
            font-size: 1.3rem;
        }

        .resource-card p {
            color: #475569;
            line-height: 1.55;
        }

        .resource-kicker {
            margin: 0;
            color: #0369a1;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            font-weight: 700;
        }

        .admin-panel {
            margin: 1rem 0 0.75rem 0;
            padding: 1rem 1.1rem;
            border-radius: 14px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
        }

        .admin-panel h3 {
            margin: 0.2rem 0 0.4rem 0;
            color: #0f172a;
        }

        .admin-panel p {
            margin: 0;
            color: #334155;
        }

        .admin-kicker {
            margin: 0;
            color: #0f766e !important;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            font-weight: 700;
        }

        [data-testid="stFileUploader"] {
            padding: 0.85rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.9);
        }

        [data-testid="stTextInputRootElement"] input {
            background: rgba(255, 255, 255, 0.96);
            color: #0f172a;
        }

        [data-testid="stBaseButton-secondary"] {
            border: 1px solid rgba(15, 23, 42, 0.16);
            background: rgba(255, 255, 255, 0.9);
            color: #0f172a;
        }

        [data-testid="stBaseButton-primary"] {
            background: linear-gradient(180deg, #0f766e, #115e59);
            color: #ffffff;
            border: none;
        }

        [data-testid="stLinkButton"] a,
        [data-testid="stLinkButton"] a:visited,
        [data-testid="stLinkButton"] a:hover {
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "show_admin_panel" not in st.session_state:
    st.session_state["show_admin_panel"] = False

logo_path = BASE_DIR / "logo.png"
hero_columns = st.columns([3, 1], gap="large")
with hero_columns[0]:
    st.markdown(
        """
        <div class="hero-shell">
            <p class="hero-kicker">Apstra Lab Hub</p>
            <h1>Lab links, lab status, and DCA access in one place.</h1>
            <p class="hero-copy">
                This page is designed to be a central hub for lab participants, providing easy access to important
                resources and up-to-date lab details.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_columns[1]:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)

st.subheader("Current Lab Details")
st.caption("Visitors can view this table. Use the admin button at the bottom of the page to replace it with a new CSV.")
st.dataframe(build_display_rows(load_lab_rows()), use_container_width=True, hide_index=True)

render_link_cards()
render_admin_panel()
