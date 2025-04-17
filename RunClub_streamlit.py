import streamlit as st
import pandas as pd
import os
import random

# --- File paths for persistent storage ---
SIGNUPS_CSV = "signups.csv"
TEAMS_CSV = "teams.csv"

# --- Sample Data Functions ---
def sample_signups_df():
    sample_data = pd.DataFrame([
         {"Name": "Alice", "Email": "alice@example.com", "Age Range": "18–25", "Experience Level": "Intermediate", "Character Theme": "Mario", "Beta Interested": True, "Time": 5.21},
         {"Name": "Bob", "Email": "bob@example.com", "Age Range": "26–35", "Experience Level": "Advanced", "Character Theme": "Luigi", "Beta Interested": False, "Time": 5.29},
         {"Name": "Charlie", "Email": "charlie@example.com", "Age Range": "18–25", "Experience Level": "Beginner", "Character Theme": "Peach", "Beta Interested": True, "Time": 5.31}
    ])
    return sample_data

def sample_teams_df():
    sample_team_data = pd.DataFrame([
         {"Team Name": "Fast Runners", "Team Captain": "David", "Team Email": "david@example.com", "Team Members": "David, Emma, Liam", "Beta Interested": True},
         {"Team Name": "Speedsters", "Team Captain": "Sara", "Team Email": "sara@example.com", "Team Members": "Sara, Tom", "Beta Interested": False}
    ])
    return sample_team_data

# --- Helper Functions for CSV Operations ---
def load_signups():
    if os.path.exists(SIGNUPS_CSV):
        df = pd.read_csv(SIGNUPS_CSV)
        # Rename "Character Choice" to "Character Theme" if needed for consistency
        if "Character Choice" in df.columns:
            df.rename(columns={"Character Choice": "Character Theme"}, inplace=True)
        # If the CSV is empty, preload with sample data
        if df.empty:
            df = sample_signups_df()
            save_signups(df)
    else:
        df = sample_signups_df()
        save_signups(df)
    return df

def save_signups(df):
    df.to_csv(SIGNUPS_CSV, index=False)

def load_teams():
    if os.path.exists(TEAMS_CSV):
        df = pd.read_csv(TEAMS_CSV)
        if df.empty:
            df = sample_teams_df()
            save_teams(df)
    else:
        df = sample_teams_df()
        save_teams(df)
    return df

def save_teams(df):
    df.to_csv(TEAMS_CSV, index=False)

# --- Initialize Session State for Data Persistence ---
if "signup_data" not in st.session_state:
    st.session_state.signup_data = load_signups()
if "teams_data" not in st.session_state:
    st.session_state.teams_data = load_teams()
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Sidebar Navigation & Theme Toggle ---
st.sidebar.title("🏁 Run Dome Navigation")
# Dark/Light theme toggle
theme_choice = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme_choice == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #FFFFFF;
        }
        .stMarkdown, .stHeader, .stSidebar, .stTitle { 
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Navigation
st.sidebar.radio("Select a Page", ["Home", "Team Registration"], key="page")

st.sidebar.header("Sign-Up Stats 📊")
if not st.session_state.signup_data.empty:
    theme_counts = st.session_state.signup_data["Character Theme"].value_counts()
    for theme, count in theme_counts.items():
        st.sidebar.markdown(f"**{theme}**: {count}")
else:
    st.sidebar.markdown("No sign-ups yet! Be the first to join! 🎉")

# --- Page Routing ---
page = st.session_state.page

if page == "Home":
    st.title("This Week:")
    st.title("The Real-Life Mario Kart Game")
    st.markdown(
        """
Welcome to **Run Dome Beta** – where running meets the thrill of a gaming adventure!  
Prepare for a fun, **gamified running experience** with exciting power-ups, challenging obstacles, and unique track themes.  
Whether you're an avid runner or looking to try something new, join our beta and be part of the action! 🚀🏃‍♀️💨
        """
    )
    st.divider()

    # Layout: Two-column layout for sign-up form and what-to-expect info
    col1, col2 = st.columns(2)
    with col1:
        st.header("Sign Up Now")
        with st.form(key="signup_form"):
            name = st.text_input("Name", help="Enter your full name")
            email = st.text_input("Email", help="We'll send updates and beta details here")
            age_range = st.selectbox("Age Range", options=["Under 18", "18–25", "26–35", "36–50", "50+"], help="Select your age range")
            experience = st.radio("Experience Level", options=["Beginner", "Intermediate", "Advanced"], help="Your current running experience")
            character_theme = st.selectbox("Character Theme", options=["Mario", "Luigi", "Bowser", "Peach", "Goomba", "Daisy", "Donkey Kong", "Koopa Troopa", "Yoshi", "Shy Guy", "Bowser Jr.", "Wario", "Waluigi", "Funky Kong"], help="Choose your in-game character theme")
            beta_interest = st.checkbox("Interested in beta testing power-ups and immersive gear", help="Get early access to game features by checking this")
            submit = st.form_submit_button("Submit")
        
        if submit:
            new_time = random.randint(0, 100)
            new_entry = {
                "Name": name,
                "Email": email,
                "Age Range": age_range,
                "Experience Level": experience,
                "Character Theme": character_theme,
                "Beta Interested": beta_interest,
                "Time": new_time
            }
            new_entry_df = pd.DataFrame([new_entry])
            st.session_state.signup_data = pd.concat([st.session_state.signup_data, new_entry_df], ignore_index=True)
            save_signups(st.session_state.signup_data)
            st.success("Thanks for signing up! Your registration has been recorded. 🎉")
    with col2:
        st.header("What to Expect")
        st.markdown(
            """
**Exciting Race Formats:**
- **🎢 Thrilling Tracks:** Navigate dynamic courses with fun challenges.
- **🚀 Power-Ups & Obstacles:** Earn boosts and overcome obstacles.
- **👟 Immersive Experience:** Get ready for tech enhancements and exclusive gear.

Stay tuned for updates on race events, tech upgrades, and special beta events!
            """
        )
    st.divider()


elif page == "Team Registration":
    st.title("👥 Team Registration")
    st.markdown("Register as an individual or gather your crew for a group running adventure!")
    
    with st.form(key="team_form"):
        team_name = st.text_input("Team Name", help="Enter your team's name")
        team_captain = st.text_input("Team Captain", help="Enter the captain's name (if applicable)")
        team_email = st.text_input("Team Email", help="A contact email for your team")
        team_members = st.text_area("Team Members", help="List your team members separated by commas (e.g., John, Jane, Doe)")
        beta_interest_team = st.checkbox("Interested in beta testing as a team", help="Select if your team wants early beta access")
        submit_team = st.form_submit_button("Register Team")
    
    if submit_team:
        new_team = {
            "Team Name": team_name,
            "Team Captain": team_captain,
            "Team Email": team_email,
            "Team Members": team_members,
            "Beta Interested": beta_interest_team
        }
        new_team_df = pd.DataFrame([new_team])
        st.session_state.teams_data = pd.concat([st.session_state.teams_data, new_team_df], ignore_index=True)
        save_teams(st.session_state.teams_data)
        st.success("Team registered successfully! 🎉")
    
    if not st.session_state.teams_data.empty:
        st.markdown("### Registered Teams")
        st.dataframe(st.session_state.teams_data.reset_index(drop=True))
        
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>© 2025 Run Dome Beta | Contact: <a href='mailto:beta@rundome.com'>beta@rundome.com</a></p>", unsafe_allow_html=True)
