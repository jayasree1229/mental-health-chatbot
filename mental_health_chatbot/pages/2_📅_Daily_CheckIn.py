import streamlit as st
import datetime
import pandas as pd
import altair as alt
import numpy as np
import calendar
import time
from datetime import timedelta

# Import necessary modules
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple sidebar
with st.sidebar:
    st.write("Welcome to Mental Health Companion!")

# Get today's date
today = datetime.date.today()

# Initialize necessary session state variables
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = today



# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    padding: 0;
    margin: 0;
}

/* Show header with light blue background */
.stApp header {
    background: #E6F2FF;
    color: #2C3E50;
    padding: 0;
    margin: 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #2C3E50;
}

p, li {
    font-family: 'Poppins', sans-serif;
    color: #34495E;
    line-height: 1.6;
}

/* Section styling without containers */
.section {
    padding: 20px 0;
    margin: 20px 0;
    border-bottom: 1px solid #eaeaea;
}

.section:last-child {
    border-bottom: none;
}

/* Button styling */
.stButton button {
    background: linear-gradient(90deg, #3498DB 0%, #2980B9 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: linear-gradient(90deg, #2980B9 0%, #3498DB 100%);
    box-shadow: 0 4px 15px rgba(41, 128, 185, 0.4);
    transform: translateY(-2px);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load previous mood data (or create an empty DataFrame if no data exists)
try:
    mood_data = pd.read_csv("mood_data.csv")
except FileNotFoundError:
    mood_data = pd.DataFrame(columns=["Date", "Mood", "Notes"])

# Display mood check-in interface with gradient title
st.markdown('<h1 style="background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; margin-bottom: 1rem;">Daily Wellness Check-in</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 30px;">
    <p style="font-size: 1.1rem;">Track your emotional wellbeing and see your progress over time.</p>
</div>
""", unsafe_allow_html=True)

# Create a section for the check-in form
st.markdown('<div class="section">', unsafe_allow_html=True)

st.markdown('<h3 style="margin-bottom: 20px; text-align: center;">How are you feeling today?</h3>', unsafe_allow_html=True)

# Date selection with calendar and past entries
col1, col2 = st.columns([3, 1])

# Initialize session state for selected date if not exists
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = today

with col2:
    # Show today's date in a nice format
    st.markdown(f'<div style="background-color: #f8f9fa; border-radius: 12px; padding: 15px; text-align: center;"><p style="margin: 0; font-size: 0.9rem;">Today: {today.strftime("%B %d, %Y")}</p></div>', unsafe_allow_html=True)

    # Option to select a different date
    selected_date = st.date_input("Select date", st.session_state.selected_date, max_value=today)
    st.session_state.selected_date = selected_date

    # When the date is changed, the entry for that date will automatically load
    # No need for additional UI elements for loading entries

# Mood selection with expanded options and visual indicators
with col1:
    st.markdown('<h4 style="margin-bottom: 15px;">Select your mood:</h4>', unsafe_allow_html=True)

    # Create a more visually appealing mood selector
    mood_options = [
        "😄 Great",
        "😊 Good",
        "😐 Neutral",
        "😕 Meh",
        "😔 Sad",
        "😫 Stressed",
        "😡 Angry"
    ]

    # Check if there's existing data for the selected date
    existing_entry = None
    if not mood_data.empty:
        # Convert date strings to datetime objects if needed
        mood_data_check = mood_data.copy()
        if not isinstance(mood_data_check['Date'].iloc[0], datetime.date):
            mood_data_check['Date'] = pd.to_datetime(mood_data_check['Date'])

        # Filter for the selected date
        existing_entries = mood_data_check[mood_data_check['Date'].dt.date == selected_date]
        if not existing_entries.empty:
            existing_entry = existing_entries.iloc[0]

    # Initialize or update selected_mood based on existing entry
    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None

    # If viewing an existing entry, set the mood from that entry
    if existing_entry is not None and st.session_state.selected_date != today:
        st.session_state.selected_mood = existing_entry['Mood']

    # Create mood selection with color indicators
    mood_cols = st.columns(len(mood_options))

    for i, mood_option in enumerate(mood_options):
        with mood_cols[i]:
            mood_emoji = mood_option.split()[0]
            mood_name = mood_option.split()[1]

            # Create a button for each mood with appropriate styling
            if st.session_state.selected_mood == mood_option:
                # Use primary style for selected mood
                if st.button(
                    mood_emoji + "\n" + mood_name,
                    key=f"mood_{i}",
                    use_container_width=True,
                    help=f"Select if you're feeling {mood_name}",
                    type="primary"
                ):
                    st.session_state.selected_mood = mood_option
            else:
                # Use secondary style for unselected moods
                if st.button(
                    mood_emoji + "\n" + mood_name,
                    key=f"mood_{i}",
                    use_container_width=True,
                    help=f"Select if you're feeling {mood_name}",
                    type="secondary"
                ):
                    st.session_state.selected_mood = mood_option

    # Display the selected mood
    if st.session_state.selected_mood:
        st.success(f"Selected mood: {st.session_state.selected_mood}")
        mood = st.session_state.selected_mood
    else:
        st.info("Please select a mood above")
        mood = None

# Set default values from existing entry if available
default_energy = 5
default_sleep_hours = 7
default_sleep_quality = "Fair"
default_activities = []
default_notes = ""

if existing_entry is not None:
    # Set defaults from existing entry
    if 'Energy' in existing_entry:
        default_energy = existing_entry['Energy']
    if 'Sleep_Hours' in existing_entry:
        default_sleep_hours = existing_entry['Sleep_Hours']
    if 'Sleep_Quality' in existing_entry:
        default_sleep_quality = existing_entry['Sleep_Quality']
    if 'Activities' in existing_entry and isinstance(existing_entry['Activities'], str):
        default_activities = existing_entry['Activities'].split(", ")
    if 'Notes' in existing_entry:
        default_notes = existing_entry['Notes']

# Energy level slider
st.markdown('<h4 style="margin-top: 25px; margin-bottom: 10px;">Energy Level</h4>', unsafe_allow_html=True)
# Ensure all slider values are integers
default_energy_int = int(default_energy) if isinstance(default_energy, (int, float)) else 5
energy_level = st.slider("Rate your energy level today", 1, 10, default_energy_int, help="1 = Very low energy, 10 = Very high energy")

# Sleep quality
st.markdown('<h4 style="margin-top: 25px; margin-bottom: 10px;">Sleep Quality</h4>', unsafe_allow_html=True)
# Ensure sleep hours is an integer
default_sleep_hours_int = int(default_sleep_hours) if isinstance(default_sleep_hours, (int, float)) else 7
sleep_hours = st.number_input("Hours of sleep last night", min_value=0, max_value=24, value=default_sleep_hours_int, step=1)
sleep_quality = st.select_slider(
    "How well did you sleep?",
    options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
    value=default_sleep_quality
)

# Activities that affected mood
st.markdown('<h4 style="margin-top: 25px; margin-bottom: 10px;">Activities Today</h4>', unsafe_allow_html=True)
st.markdown('<p style="margin-bottom: 15px; font-size: 0.9rem; color: #666;">Select activities that affected your mood today:</p>', unsafe_allow_html=True)

activities_col1, activities_col2 = st.columns(2)

with activities_col1:
    # Use default values from existing entry
    exercise = st.checkbox("Exercise", value="Exercise" in default_activities)
    meditation = st.checkbox("Meditation/Mindfulness", value="Meditation/Mindfulness" in default_activities)
    social = st.checkbox("Social Interaction", value="Social Interaction" in default_activities)
    work = st.checkbox("Work/Study", value="Work/Study" in default_activities)

with activities_col2:
    # Use default values from existing entry
    nature = st.checkbox("Time in Nature", value="Time in Nature" in default_activities)
    creative = st.checkbox("Creative Activities", value="Creative Activities" in default_activities)
    screen = st.checkbox("Screen Time", value="Screen Time" in default_activities)
    other = st.checkbox("Other", value="Other" in default_activities)

# Notes section with improved guidance
st.markdown('<h4 style="margin-top: 25px; margin-bottom: 10px;">Journal Entry</h4>', unsafe_allow_html=True)
st.markdown('<p style="margin-bottom: 15px; font-size: 0.9rem; color: #666;">Reflect on your day and how you\'re feeling. What went well? What challenges did you face? What are you grateful for today?</p>', unsafe_allow_html=True)

# Use the default value from existing entry
notes = st.text_area("Your thoughts", value=default_notes, placeholder="Write here...", height=150, label_visibility="collapsed")

# Get activities as a list
selected_activities = []
if exercise: selected_activities.append("Exercise")
if meditation: selected_activities.append("Meditation/Mindfulness")
if social: selected_activities.append("Social Interaction")
if work: selected_activities.append("Work/Study")
if nature: selected_activities.append("Time in Nature")
if creative: selected_activities.append("Creative Activities")
if screen: selected_activities.append("Screen Time")
if other: selected_activities.append("Other")

# Create a section for the submit button
st.markdown('<div style="margin-top: 30px; margin-bottom: 20px;">', unsafe_allow_html=True)

# Add a flag to track if we should refresh the page
if 'refresh_page' not in st.session_state:
    st.session_state.refresh_page = False

# If the refresh flag is set, clear it and refresh the page
if st.session_state.refresh_page:
    st.session_state.refresh_page = False
    st.rerun()

# Submit button with simple styling
if st.button("Save Check-in", use_container_width=True, type="primary"):
    if mood is None:
        st.error("Please select a mood before saving your check-in.")
    else:
        # Create a more comprehensive data entry
        new_data = {
            "Date": selected_date,
            "Mood": mood,
            "Energy": energy_level,
            "Sleep_Hours": sleep_hours,
            "Sleep_Quality": sleep_quality,
            "Activities": ", ".join(selected_activities) if selected_activities else "None",
            "Notes": notes
        }

        # Check if there's already an entry for this date
        existing_entry_found = False
        if not mood_data.empty:
            # Convert date strings to datetime objects if needed
            mood_data_check = mood_data.copy()
            if not isinstance(mood_data_check['Date'].iloc[0], datetime.date):
                mood_data_check['Date'] = pd.to_datetime(mood_data_check['Date'])

            # Check if there's already an entry for this date
            existing_entry_found = (mood_data_check['Date'].dt.date == selected_date).any()

        if existing_entry_found:
            # Remove the existing entry - handle both string and datetime formats
            if isinstance(mood_data['Date'].iloc[0], datetime.date) or isinstance(mood_data['Date'].iloc[0], pd.Timestamp):
                mood_data = mood_data[mood_data['Date'].dt.date != selected_date]
            else:
                mood_data = mood_data[mood_data["Date"] != str(selected_date)]

            # Add the new entry
            mood_data = pd.concat([mood_data, pd.DataFrame([new_data])], ignore_index=True)
            mood_data.to_csv("mood_data.csv", index=False)
            st.success(f"Check-in updated for {selected_date.strftime('%B %d, %Y')}")
        else:
            # Add the new entry
            mood_data = pd.concat([mood_data, pd.DataFrame([new_data])], ignore_index=True)
            mood_data.to_csv("mood_data.csv", index=False)
            st.success(f"Check-in saved for {selected_date.strftime('%B %d, %Y')}")

        # Set the refresh flag to trigger a page reload on the next run
        st.session_state.refresh_page = True
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Display mood tracking visualization in a section
if not mood_data.empty:
    st.markdown('<div class="section" style="margin-top: 40px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin-bottom: 20px;">Your Mood Tracker</h2>', unsafe_allow_html=True)

    # Create tabs for different views
    history_tab, charts_tab, insights_tab, calendar_tab = st.tabs(["History", "Charts", "Insights", "Calendar"])

    # Convert date strings to datetime objects for proper sorting
    mood_data['Date'] = pd.to_datetime(mood_data['Date'])

    # Sort by date
    mood_data = mood_data.sort_values('Date')

    with history_tab:
        # Convert back to string for display
        display_data = mood_data.copy()
        display_data['Date'] = display_data['Date'].dt.strftime('%Y-%m-%d')

        # Format the data for better display
        display_data = display_data.sort_values('Date', ascending=False)  # Most recent entries first

        # Rename columns for better readability
        display_data = display_data.rename(columns={
            'Sleep_Hours': 'Sleep (hrs)',
            'Sleep_Quality': 'Sleep Quality',
        })

        # Truncate long text in Activities and Notes columns
        display_data['Activities'] = display_data['Activities'].apply(lambda x: (x[:40] + '...') if isinstance(x, str) and len(x) > 40 else x)
        display_data['Notes'] = display_data['Notes'].apply(lambda x: (x[:50] + '...') if isinstance(x, str) and len(x) > 50 else x)

        # Calculate the height based on the number of rows (with a minimum and maximum)
        num_rows = len(display_data)
        table_height = max(300, min(600, 100 + num_rows * 35))  # 35px per row, min 300px, max 600px

        # Use the height parameter to make the table expand according to data
        st.dataframe(
            display_data[['Date', 'Mood', 'Energy', 'Sleep (hrs)', 'Sleep Quality', 'Activities', 'Notes']],
            use_container_width=True,
            height=table_height,
            column_config={
                "Date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
                "Mood": st.column_config.TextColumn("Mood"),
                "Energy": st.column_config.NumberColumn("Energy", format="%d/10"),
                "Sleep (hrs)": st.column_config.NumberColumn("Sleep (hrs)", format="%d hrs"),
                "Activities": st.column_config.TextColumn("Activities"),
                "Notes": st.column_config.TextColumn("Journal Entry")
            }
        )

    with charts_tab:
        # Create a mood mapping for numerical values
        mood_mapping = {
            "😄 Great": 7,
            "😊 Good": 6,
            "😐 Neutral": 5,
            "😕 Meh": 4,
            "😔 Sad": 3,
            "😫 Stressed": 2,
            "😡 Angry": 1
        }

        # Create a copy of the dataframe for charts
        chart_data = mood_data.copy()

        # Add a numerical mood value
        chart_data['Mood_Value'] = chart_data['Mood'].map(lambda x: next((v for k, v in mood_mapping.items() if k == x), 5))

        # Create a date range for the last 30 days
        end_date = datetime.date.today()
        start_date = end_date - timedelta(days=30)

        # Filter data for the last 30 days
        recent_data = chart_data[chart_data['Date'] >= pd.Timestamp(start_date)]

        # Create mood trend chart
        st.subheader("Mood Trend (Last 30 Days)")

        if not recent_data.empty:
            # Count the occurrences of each mood
            mood_counts = chart_data["Mood"].value_counts()
            st.bar_chart(mood_counts, use_container_width=True)

            if len(recent_data) > 1:
                # Create the line chart for mood trends
                st.line_chart(recent_data.set_index("Date")["Mood_Value"], use_container_width=True)

                # Create correlation charts
                st.subheader("Correlations")

                col1, col2 = st.columns(2)

                with col1:
                    # Sleep vs Mood
                    if 'Sleep_Hours' in recent_data.columns:
                        st.subheader("Sleep vs Mood")
                        sleep_mood_data = recent_data[['Date', 'Sleep_Hours', 'Mood_Value']]
                        sleep_mood_data = sleep_mood_data.rename(columns={'Mood_Value': 'Mood Rating'})
                        st.scatter_chart(sleep_mood_data.set_index('Date'), x='Sleep_Hours', y='Mood Rating', use_container_width=True)

                with col2:
                    # Energy vs Mood
                    if 'Energy' in recent_data.columns:
                        st.subheader("Energy vs Mood")
                        energy_mood_data = recent_data[['Date', 'Energy', 'Mood_Value']]
                        energy_mood_data = energy_mood_data.rename(columns={'Mood_Value': 'Mood Rating'})
                        st.scatter_chart(energy_mood_data.set_index('Date'), x='Energy', y='Mood Rating', use_container_width=True)
        else:
            st.info("Not enough data for charts. Log your mood for a few days to see trends.")

    with insights_tab:
        st.subheader("Mood Insights")

        if len(chart_data) >= 3:  # Only show insights if we have enough data
            # Calculate average mood
            if 'Mood_Value' in chart_data.columns:
                avg_mood_value = chart_data['Mood_Value'].mean()
                avg_mood_text = "Positive" if avg_mood_value > 5 else "Neutral" if avg_mood_value == 5 else "Negative"

                # Calculate mood stability (standard deviation)
                mood_stability = chart_data['Mood_Value'].std()
                stability_text = "Very stable" if mood_stability < 1 else "Somewhat stable" if mood_stability < 2 else "Variable"

                # Find activities correlation with good moods
                good_mood_days = chart_data[chart_data['Mood_Value'] >= 6]
                good_mood_activities = []

                if 'Activities' in good_mood_days.columns:
                    for _, row in good_mood_days.iterrows():
                        if isinstance(row['Activities'], str):
                            activities = row['Activities'].split(", ")
                            good_mood_activities.extend(activities)

                # Count activity frequencies
                from collections import Counter
                activity_counts = Counter(good_mood_activities)

                # Display insights
                st.markdown(f"**Overall Mood Trend:** {avg_mood_text}")
                st.markdown(f"**Mood Stability:** {stability_text}")

                if activity_counts and 'None' not in activity_counts:
                    # Find most common activities on good days
                    most_common = activity_counts.most_common(3)
                    st.markdown("**Activities associated with better mood:**")
                    for activity, count in most_common:
                        st.markdown(f"- {activity}")

                # Sleep insights
                if 'Sleep_Hours' in chart_data.columns:
                    avg_sleep = chart_data['Sleep_Hours'].mean()
                    st.markdown(f"**Average Sleep:** {avg_sleep:.1f} hours per night")

                # Personalized recommendations
                st.subheader("Personalized Recommendations")

                if avg_mood_value < 5:
                    st.markdown("Based on your mood patterns:")
                    st.markdown("- Consider speaking with a mental health professional")
                    st.markdown("- Try incorporating more physical activity into your routine")
                    st.markdown("- Practice mindfulness or meditation daily")

                if 'Sleep_Hours' in chart_data.columns and avg_sleep < 7:
                    st.markdown("Your sleep patterns suggest:")
                    st.markdown("- Try to increase your sleep time to 7-8 hours")
                    st.markdown("- Establish a regular sleep schedule")
                    st.markdown("- Reduce screen time before bed")

                # Add activity recommendations based on good mood correlations
                if activity_counts:
                    st.markdown("Activities that might improve your mood:")
                    for activity, _ in activity_counts.most_common(3):
                        if activity != "None":
                            st.markdown(f"- Do more {activity.lower()}")
        else:
            st.info("Not enough data for insights. Continue logging your mood daily to receive personalized insights.")

    with calendar_tab:
        st.subheader("Mood Calendar")

        # Get the current month and year
        if 'calendar_month' not in st.session_state:
            st.session_state.calendar_month = today.month
        if 'calendar_year' not in st.session_state:
            st.session_state.calendar_year = today.year

        # Month navigation
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("◀ Prev"):
                if st.session_state.calendar_month == 1:
                    st.session_state.calendar_month = 12
                    st.session_state.calendar_year -= 1
                else:
                    st.session_state.calendar_month -= 1

        with col2:
            st.markdown(f"<h4 style='text-align: center;'>{calendar.month_name[st.session_state.calendar_month]} {st.session_state.calendar_year}</h4>", unsafe_allow_html=True)

        with col3:
            if st.button("Next ▶"):
                if st.session_state.calendar_month == 12:
                    st.session_state.calendar_month = 1
                    st.session_state.calendar_year += 1
                else:
                    st.session_state.calendar_month += 1

        # Create a calendar view
        cal = calendar.monthcalendar(st.session_state.calendar_year, st.session_state.calendar_month)

        # Create a mapping of dates to moods for the current month
        month_data = chart_data[
            (chart_data['Date'].dt.month == st.session_state.calendar_month) &
            (chart_data['Date'].dt.year == st.session_state.calendar_year)
        ]

        date_to_mood = {}
        for _, row in month_data.iterrows():
            date_to_mood[row['Date'].day] = row['Mood']

        # Display the calendar
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

        # Day headers
        cols = st.columns(7)
        for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            cols[i].markdown(f"<div style='text-align: center; font-weight: bold;'>{day}</div>", unsafe_allow_html=True)

        # Calendar days
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    cols[i].markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
                else:
                    # Get the mood for this day if it exists
                    mood_emoji = ""
                    if day in date_to_mood:
                        mood_emoji = date_to_mood[day].split()[0]  # Get just the emoji

                    # Highlight today
                    if (day == today.day and
                        st.session_state.calendar_month == today.month and
                        st.session_state.calendar_year == today.year):
                        cols[i].markdown(f"<div style='text-align: center; background-color: #e6f2ff; border-radius: 5px; padding: 5px;'><div style='font-weight: bold;'>{day}</div><div style='font-size: 1.5em;'>{mood_emoji}</div></div>", unsafe_allow_html=True)
                    else:
                        cols[i].markdown(f"<div style='text-align: center; padding: 5px;'><div>{day}</div><div style='font-size: 1.5em;'>{mood_emoji}</div></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="section" style="margin-top: 40px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin-bottom: 20px;">Your Mood Tracker</h2>', unsafe_allow_html=True)
    st.info("No mood data recorded yet. Start by logging your mood above!")
    st.markdown('</div>', unsafe_allow_html=True)


