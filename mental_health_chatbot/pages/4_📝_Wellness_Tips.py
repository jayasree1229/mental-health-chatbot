import streamlit as st
import json
import os
import datetime

# Import necessary modules
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple sidebar
with st.sidebar:
    st.write("Welcome to Mental Health Companion!")

# Function to save habit data to a file
def save_habit_data_to_file():
    # Create a directory for user data if it doesn't exist
    if not os.path.exists("user_data"):
        os.makedirs("user_data")

    # Create a file path for the guest user
    file_path = "user_data/Guest_habits.json"

    # Convert datetime.date objects to strings for JSON serialization
    serializable_data = {}
    for date, data in st.session_state.habit_data.items():
        if isinstance(date, datetime.date):
            date_str = date.isoformat()
        else:
            date_str = str(date)
        serializable_data[date_str] = data

    # Save the data to the file
    with open(file_path, "w") as f:
        json.dump(serializable_data, f)

# Function to load habit data from a file
def load_habit_data_from_file():
    file_path = "user_data/Guest_habits.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            serialized_data = json.load(f)

        # Convert string dates back to datetime.date objects
        deserialized_data = {}
        for date_str, data in serialized_data.items():
            try:
                # Try to parse as ISO format date
                date_obj = datetime.date.fromisoformat(date_str)
            except ValueError:
                # If that fails, keep as string
                date_obj = date_str
            deserialized_data[date_obj] = data

        return deserialized_data

    return {}

# Function to check if a habit checkbox should be checked
def is_habit_checked(habit_index, day_index):
    key = f"habit_{habit_index}_{day_index}"

    # First check if the key exists in session state (from current session)
    if key in st.session_state:
        return st.session_state[key]

    # Then check if it exists in saved data for the selected date
    if selected_date in st.session_state.habit_data:
        if key in st.session_state.habit_data[selected_date]:
            return st.session_state.habit_data[selected_date][key]

    # Default to unchecked
    return False

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

/* Card container */
.card-container {
    background-color: white;
    border-radius: 12px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Page title with gradient
st.markdown('<h1 style="background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; margin-bottom: 1rem;">Daily Wellness Tips</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 30px;">
    <p style="font-size: 1.1rem;">Incorporate these simple practices into your daily routine to support your mental wellbeing.</p>
</div>
""", unsafe_allow_html=True)


daily_tips = [
    {"title": "Morning Mindfulness", "content": "Start your day with 5 minutes of deep breathing or meditation to set a positive tone for the day. Focus on your breath and set an intention for how you want to feel.", "icon": "💤"},
    {"title": "Movement Break", "content": "Take short movement breaks throughout the day - even a 5-minute walk can boost your mood and energy. Try to get outside if possible for added benefits from natural light and fresh air.", "icon": "🏃"},
    {"title": "Gratitude Practice", "content": "End each day by writing down 3 things you're grateful for to train your brain to notice the positive. Be specific about what you appreciate and why it matters to you.", "icon": "📝"},
    {"title": "Digital Detox", "content": "Set aside time each day to disconnect from screens and be fully present in the moment. Try putting your phone in another room during meals or for an hour before bedtime.", "icon": "📱"},
    {"title": "Connect Meaningfully", "content": "Have at least one meaningful conversation each day, even if it's brief. Ask open-ended questions and practice active listening without planning your response.", "icon": "💬"},
    {"title": "Hydration", "content": "Drink plenty of water throughout the day - dehydration can affect your mood and energy levels. Try keeping a water bottle visible as a reminder to sip regularly.", "icon": "💧"}
]

# Display tips in a grid
col1, col2 = st.columns(2)

for i, tip in enumerate(daily_tips):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 15px; height: 100%;">
            <h3 style="color: #3498DB; margin-bottom: 10px; font-size: 1.3rem;">{tip['icon']} {tip['title']}</h3>
            <p style="font-size: 1rem;">{tip['content']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Weekly Wellness Practices</h2>', unsafe_allow_html=True)

weekly_practices = [
    {"title": "Digital Sabbath", "content": "Choose one day a week to disconnect from technology as much as possible. Use this time to connect with nature, loved ones, or engage in screen-free activities.", "icon": "🔌"},
    {"title": "Meal Planning", "content": "Take time each week to plan nutritious meals. This reduces decision fatigue and makes it easier to eat foods that support your mental and physical health.", "icon": "🥗"},
    {"title": "Learning Something New", "content": "Dedicate time each week to learn something new, whether it's a skill, language, or topic of interest. This keeps your mind engaged and creates a sense of accomplishment.", "icon": "📚"},
    {"title": "Social Connection", "content": "Schedule at least one meaningful social interaction each week. This could be a coffee date, phone call, or shared activity with someone whose company you enjoy.", "icon": "👥"}
]

# Display weekly practices
col1, col2 = st.columns(2)

for i, practice in enumerate(weekly_practices):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 15px; height: 100%;">
            <h3 style="color: #3498DB; margin-bottom: 10px; font-size: 1.3rem;">{practice['icon']} {practice['title']}</h3>
            <p style="font-size: 1rem;">{practice['content']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<h2 style="margin-bottom: 20px; color: #2C3E50;">Wellness Habit Tracker</h2>', unsafe_allow_html=True)
st.markdown('<p style="margin-bottom: 25px;">Track your wellness habits to build consistency and see your progress over time.</p>', unsafe_allow_html=True)

# Create a simple habit tracker
habits = [
    "Morning meditation/deep breathing",
    "Drank enough water (8 glasses)",
    "Took movement breaks",
    "Practiced gratitude",
    "Limited screen time",
    "Had a meaningful conversation",
    "Got 7-8 hours of sleep"
]

# Add date selection
col1, col2 = st.columns([3, 1])
with col1:
    selected_date = st.date_input("Select date:", help="Choose a date to track your habits")

# Initialize session state for tracking progress if not exists
if 'habit_data' not in st.session_state:
    # Load habit data from file if it exists
    st.session_state.habit_data = load_habit_data_from_file()

# Function to check all habits for the selected date
def check_all_habits():
    # Set all checkboxes to checked for the selected date
    for i in range(len(habits)):
        for j in range(1, 8):
            key = f"habit_{i}_{j}"
            st.session_state[key] = True

            # Also update the habit_data for the selected date
            if selected_date not in st.session_state.habit_data:
                st.session_state.habit_data[selected_date] = {}
            st.session_state.habit_data[selected_date][key] = True

    # Save to file immediately
    save_habit_data_to_file()

# Add a "Check All" button
with col2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("Check All", use_container_width=True):
        check_all_habits()
        st.success("All habits marked as completed!")
        st.rerun()

# No duplicate initialization needed here

# Create columns for days of the week
st.markdown('<div style="border: 1px solid #e6e6e6; border-radius: 8px; padding: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)

# Create a header row with columns
header_cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1])

# Headers - using custom CSS to align with checkboxes and improve appearance
header_cols[0].markdown("<p style='font-weight: bold; margin-left: 9px; font-size: 1rem; color: #2C3E50;'>Habit</p>", unsafe_allow_html=True)

# For day headers, add custom styling to align with checkboxes
for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    # The checkbox is centered in its column, so we center the text and adjust margins
    header_cols[i+1].markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 32px;">
        <p style='font-weight: bold; margin: 0; padding: 0; font-size: 0.9rem; color: #2C3E50;'>{day}</p>
    </div>
    """, unsafe_allow_html=True)

header_cols[8].markdown("""
<div style="display: flex; justify-content: center; align-items: center; height: 32px;">
    <p style='font-weight: bold; margin: 0; padding: 0; font-size: 0.9rem; color: #2C3E50;'>Weekly</p>
</div>
""", unsafe_allow_html=True)

# Add a separator
st.markdown("<hr style='margin: 0 0 15px 0; border: 0; border-top: 1px solid #eaeaea;'>", unsafe_allow_html=True)



# Habit rows
for i, habit in enumerate(habits):
    # Create a row with columns for each habit
    row_cols = st.columns([3, 1, 1, 1, 1, 1, 1, 1, 1])

    # Display habit name in first column with better styling
    row_cols[0].markdown(f"""
    <div style="padding: 8px 0 8px 10px;">
        <p style='margin: 0; color: #34495E; font-size: 0.95rem;'>{habit}</p>
    </div>
    """, unsafe_allow_html=True)

    # Track completed days for this habit
    completed_days = 0

    # Add checkboxes for each day
    for j in range(7):
        with row_cols[j+1]:
            # Create checkbox for each day with initial value from saved data
            checked = st.checkbox(f"Day {j+1}",
                                 key=f"habit_{i}_{j+1}",
                                 value=is_habit_checked(i, j+1),
                                 label_visibility="collapsed")

            # Count completed days
            if checked:
                completed_days += 1

    # Show weekly progress in last column
    progress_percentage = int((completed_days / 7) * 100)
    progress_color = "#2ECC71" if progress_percentage >= 70 else "#F39C12" if progress_percentage >= 40 else "#E74C3C"

    with row_cols[8]:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 40px;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: conic-gradient({progress_color} {progress_percentage}%, #f1f1f1 0); display: flex; align-items: center; justify-content: center;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background-color: white; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 500;">{progress_percentage}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add a subtle separator between habits
    if i < len(habits) - 1:
        st.markdown("<hr style='margin: 5px 0; border: 0; border-top: 1px solid #f5f5f5;'>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Daily Progress Section
st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; color: #2C3E50;">Progress Overview</h3>', unsafe_allow_html=True)

# Create columns for daily progress
col1, col2 = st.columns([1, 1])

with col1:
    # Calculate daily progress
    total_habits = len(habits)
    weekday = selected_date.weekday()
    completed_today = sum(1 for i in range(total_habits) if st.session_state.get(f"habit_{i}_{weekday + 1}", False))
    daily_percentage = int((completed_today / total_habits) * 100) if total_habits > 0 else 0

    # Display daily progress
    st.markdown(f"""
    <div style="border: 1px solid #e6e6e6; border-radius: 8px; padding: 20px; text-align: center;">
        <h4 style="margin-bottom: 15px; color: #2C3E50;">Today's Progress</h4>
        <div style="width: 120px; height: 120px; margin: 0 auto; border-radius: 50%; background: conic-gradient(#3498DB {daily_percentage}%, #f1f1f1 0); display: flex; align-items: center; justify-content: center; position: relative;">
            <div style="width: 100px; height: 100px; border-radius: 50%; background-color: white; display: flex; align-items: center; justify-content: center;">
                <div style="font-size: 1.5rem; font-weight: 600; color: #3498DB;">{daily_percentage}%</div>
            </div>
        </div>
        <p style="margin-top: 15px; color: #7f8c8d;">Completed {completed_today} of {total_habits} habits</p>
        <p style="margin-top: 5px; font-size: 0.9rem; color: #7f8c8d;">Selected day: {selected_date.strftime('%A, %B %d')}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Display weekly overview
    st.markdown("""
    <div style="border: 1px solid #e6e6e6; border-radius: 8px; padding: 20px;">
        <h4 style="margin-bottom: 15px; color: #2C3E50; text-align: center;">Weekly Overview</h4>
    """, unsafe_allow_html=True)

    # Calculate weekly stats
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for i, day in enumerate(days):
        # Highlight the current day
        is_current_day = i == weekday
        day_style = "font-weight: 600; color: #3498DB;" if is_current_day else "color: #34495E;"

        # Calculate completion for this day
        day_completed = sum(1 for h in range(len(habits)) if st.session_state.get(f"habit_{h}_{i+1}", False))
        day_percentage = int((day_completed / total_habits) * 100) if total_habits > 0 else 0
        bar_color = "#2ECC71" if day_percentage >= 70 else "#F39C12" if day_percentage >= 40 else "#E74C3C"

        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="width: 80px; font-size: 0.9rem; {day_style}">{day}</div>
            <div style="flex-grow: 1; height: 10px; background-color: #f1f1f1; border-radius: 5px; overflow: hidden;">
                <div style="width: {day_percentage}%; height: 100%; background-color: {bar_color};"></div>
            </div>
            <div style="width: 40px; text-align: right; font-size: 0.9rem;">{day_percentage}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Calculate overall weekly progress
    all_checked = sum(1 for i in range(total_habits) for j in range(1, 8) if st.session_state.get(f"habit_{i}_{j}", False))
    total_possible = total_habits * 7
    weekly_percentage = int((all_checked / total_possible) * 100) if total_possible > 0 else 0

    st.markdown(f"""
    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eaeaea;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 500; color: #2C3E50;">Overall Weekly:</div>
            <div style="font-weight: 600; color: #3498DB; font-size: 1.1rem;">{weekly_percentage}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Save button with better positioning
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Save Progress", type="primary", use_container_width=True):
        # Store in session state
        for i, habit in enumerate(habits):
            for j in range(1, 8):
                key = f"habit_{i}_{j}"
                # Make sure the key exists in session state
                if key in st.session_state:
                    # Make sure the date entry exists
                    if selected_date not in st.session_state.habit_data:
                        st.session_state.habit_data[selected_date] = {}
                    # Save the checkbox state
                    st.session_state.habit_data[selected_date][key] = st.session_state[key]

        # Save to file for persistence between sessions
        save_habit_data_to_file()
        st.success("Your progress has been saved!")

        # No need to rerun as we're just saving the current state

st.markdown('</div>', unsafe_allow_html=True)

# Resources section
st.markdown('<div style="margin-top: 40px;">', unsafe_allow_html=True)
st.markdown('<h2 style="margin-bottom: 20px; color: #2C3E50;">Wellness Resources</h2>', unsafe_allow_html=True)
st.markdown('<p style="margin-bottom: 25px;">Explore these helpful resources to support your mental wellbeing journey.</p>', unsafe_allow_html=True)

# Define resources with simpler structure
resources = [
    {
        "title": "Headspace",
        "description": "Guided meditation and mindfulness app with exercises for stress, anxiety, and sleep.",
        "url": "https://www.headspace.com/",
        "icon": "🧘‍♀️",
        "category": "Meditation"
    },
    {
        "title": "Calm",
        "description": "App for meditation, sleep stories, and relaxation techniques to reduce stress and improve sleep.",
        "url": "https://www.calm.com/",
        "icon": "😌",
        "category": "Meditation & Sleep"
    },
    {
        "title": "Insight Timer",
        "description": "Free meditation app with thousands of guided meditations and music tracks.",
        "url": "https://insighttimer.com/",
        "icon": "⏲️",
        "category": "Meditation"
    },
    {
        "title": "The Greater Good Science Center",
        "description": "Science-based insights for a meaningful life, with articles and practices for wellbeing.",
        "url": "https://greatergood.berkeley.edu/",
        "icon": "🔬",
        "category": "Research"
    },
    {
        "title": "Happify",
        "description": "Science-based activities and games to reduce stress and build resilience.",
        "url": "https://www.happify.com/",
        "icon": "😊",
        "category": "Mental Wellbeing"
    },
    {
        "title": "Ten Percent Happier",
        "description": "Meditation app with courses taught by world-renowned meditation teachers.",
        "url": "https://www.tenpercent.com/",
        "icon": "🧠",
        "category": "Meditation"
    }
]

# Create two columns for resources
col1, col2 = st.columns(2)

for i, resource in enumerate(resources):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div style="border: 1px solid #e6e6e6; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">{resource['icon']}</span>
                <h3 style="color: #3498DB; margin: 0; font-size: 1.2rem;">{resource['title']} <span style="font-size: 0.8rem; color: #999; font-weight: normal;">↗</span></h3>
            </div>
            <p style="font-size: 0.9rem; color: #777; margin: 5px 0 10px 0;">{resource['category']}</p>
            <p style="font-size: 1rem; margin: 10px 0; color: #34495E; line-height: 1.5;">{resource['description']}</p>
            <a href="{resource['url']}" target="_blank" style="color: #3498DB; text-decoration: none; display: inline-block; padding: 8px 16px; border: 1px solid #3498DB; border-radius: 4px; font-size: 0.9rem; font-weight: 500;">Visit Website</a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
