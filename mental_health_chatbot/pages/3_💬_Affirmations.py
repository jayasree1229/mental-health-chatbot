import streamlit as st
import random
import json
import os

# Import necessary modules
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple sidebar
with st.sidebar:
    st.write("Welcome to Mental Health Companion!")

# Function to save favorite affirmations to a file
def save_favorites_to_file():
    # Create a directory for user data if it doesn't exist
    if not os.path.exists("user_data"):
        os.makedirs("user_data")

    # Create a file path for the guest user
    file_path = "user_data/Guest_favorites.json"

    # Save the data to the file
    with open(file_path, "w") as f:
        json.dump(st.session_state.favorite_affirmations, f)

# Function to load favorite affirmations from a file
def load_favorites_from_file():
    file_path = "user_data/Guest_favorites.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    return []

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

/* Affirmation card */
.affirmation-card {
    background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
    color: white;
    border-radius: 12px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.affirmation-card:before {
    content: '"';
    position: absolute;
    top: 10px;
    left: 20px;
    font-size: 60px;
    opacity: 0.2;
    font-family: Georgia, serif;
}

.affirmation-card:after {
    content: '"';
    position: absolute;
    bottom: 10px;
    right: 20px;
    font-size: 60px;
    opacity: 0.2;
    font-family: Georgia, serif;
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

/* Resource cards */
.resource-card {
    background-color: #f8f9fa;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #e6e6e6;
}

.resource-card a {
    color: #3498DB;
    text-decoration: none;
    font-weight: 500;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Expanded affirmations list with categories
affirmations = {
    "confidence": [
        "You are enough just as you are.",
        "You are worthy of good things.",
        "Your potential is endless.",
        "You have the strength to overcome any challenge.",
        "You deserve to take up space in this world.",
        "Your voice matters and deserves to be heard.",
        "You are capable of amazing things.",
        "You have unique gifts that the world needs.",
        "You are becoming more confident every day.",
        "You are resilient and can handle whatever comes your way."
    ],
    "comfort": [
        "This too shall pass.",
        "Your feelings are valid.",
        "You are not alone in this.",
        "It's okay to not be okay sometimes.",
        "You are loved more than you know.",
        "You are safe in this moment.",
        "You are allowed to rest and take care of yourself.",
        "You don't have to carry everything on your own.",
        "You are surrounded by support, even when you can't see it.",
        "Your struggles do not define you."
    ],
    "growth": [
        "You are doing your best, and that's enough.",
        "Every day is a fresh start.",
        "You have the power to create change.",
        "Small steps still move you forward.",
        "You learn and grow with every experience.",
        "You are constantly evolving into a better version of yourself.",
        "Your mistakes help you learn and grow.",
        "You are exactly where you need to be right now.",
        "You have everything you need within you.",
        "Today is full of possibilities for growth."
    ]
}

# Expanded resources with better categorization and more content
resources = {
    "sad": [
        {"title": "How to Deal with Sadness", "type": "Article", "url": "https://www.psychologytoday.com/us/basics/sadness", "icon": "📝"},
        {"title": "Overcoming Sadness", "type": "Podcast", "url": "https://www.helpguide.org/articles/depression/coping-with-depression.htm", "icon": "🎧"},
        {"title": "Finding Joy in Small Things", "type": "Guide", "url": "https://www.verywellmind.com/how-to-find-happiness-4178632", "icon": "📘"},
        {"title": "Sadness vs. Depression", "type": "Video", "url": "https://www.youtube.com/watch?v=z-IR48Mb3W0", "icon": "🎬"},
        {"title": "Journaling Prompts for Sadness", "type": "Tool", "url": "https://www.healthline.com/health/depression/journal-prompts", "icon": "✏"}
    ],
    "anxious": [
        {"title": "Coping with Anxiety", "type": "Video", "url": "https://www.youtube.com/watch?v=fdBOxBohFMk", "icon": "🎬"},
        {"title": "Managing Anxiety", "type": "Article", "url": "https://www.psychologytoday.com/us/basics/anxiety", "icon": "📝"},
        {"title": "5-Minute Calming Exercises", "type": "Guide", "url": "https://www.healthline.com/health/anxiety-exercises", "icon": "📘"},
        {"title": "Anxiety Relief Meditation", "type": "Audio", "url": "https://www.youtube.com/watch?v=O-6f5wQXSu8", "icon": "🎵"},
        {"title": "Understanding Panic Attacks", "type": "Infographic", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/panic-attacks/", "icon": "📊"}
    ],
    "stressed": [
        {"title": "Stress Management Techniques", "type": "Guide", "url": "https://www.helpguide.org/articles/stress/stress-management.htm", "icon": "📘"},
        {"title": "Quick Stress Relievers", "type": "Article", "url": "https://www.verywellmind.com/tips-to-reduce-stress-3145195", "icon": "📝"},
        {"title": "Guided Stress Relief Meditation", "type": "Audio", "url": "https://www.youtube.com/watch?v=z6X5oEIg6Ak", "icon": "🎵"},
        {"title": "Progressive Muscle Relaxation", "type": "Video", "url": "https://www.youtube.com/watch?v=1nZEdqcGVzo", "icon": "🎬"},
        {"title": "Stress and Your Body", "type": "Course", "url": "https://www.coursera.org/learn/stress", "icon": "🏫"}
    ],
    "motivated": [
        {"title": "Believe in Yourself", "type": "Video", "url": "https://www.youtube.com/watch?v=H08Gn-QgYsY", "icon": "🎬"},
        {"title": "Finding Your Motivation", "type": "Article", "url": "https://www.psychologytoday.com/us/basics/motivation", "icon": "📝"},
        {"title": "Setting Achievable Goals", "type": "Guide", "url": "https://www.mindtools.com/pages/article/smart-goals.htm", "icon": "📘"},
        {"title": "Morning Motivation Routine", "type": "Podcast", "url": "https://www.ted.com/talks/mel_robbins_how_to_stop_screwing_yourself_over", "icon": "🎧"},
        {"title": "Habit Building Tracker", "type": "Tool", "url": "https://www.habitify.me/", "icon": "📱"}
    ]
}

# Page title with gradient
st.markdown('<h1 style="background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; margin-bottom: 1rem;">Daily Affirmations & Resources</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 30px;">
    <p style="font-size: 1.1rem;">Positive affirmations and helpful resources to support your mental wellbeing journey.</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<h3 style="text-align: center; margin-bottom: 20px;">Daily Affirmations</h3>', unsafe_allow_html=True)

# Initialize session state for affirmation category and text
if 'affirmation_category' not in st.session_state:
    st.session_state.affirmation_category = "confidence"
if 'current_affirmation' not in st.session_state:
    st.session_state.current_affirmation = random.choice(affirmations[st.session_state.affirmation_category])
if 'favorite_affirmations' not in st.session_state:
    # Load favorite affirmations from file if it exists
    st.session_state.favorite_affirmations = load_favorites_from_file()

# Function to update affirmation based on category
def update_affirmation():
    st.session_state.current_affirmation = random.choice(affirmations[st.session_state.affirmation_category])

# Function to add to favorites
def add_to_favorites():
    if st.session_state.current_affirmation not in st.session_state.favorite_affirmations:
        st.session_state.favorite_affirmations.append(st.session_state.current_affirmation)
        # Save to file for persistence between sessions
        save_favorites_to_file()

# Function to change category
def change_category(category):
    st.session_state.affirmation_category = category
    update_affirmation()

# Category selection tabs with icons
st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    confidence_selected = st.button("✨ Confidence",
                                   key="confidence_btn",
                                   use_container_width=True,
                                   type="primary" if st.session_state.affirmation_category == "confidence" else "secondary")
    if confidence_selected:
        change_category("confidence")

with col2:
    comfort_selected = st.button("🌈 Comfort",
                                key="comfort_btn",
                                use_container_width=True,
                                type="primary" if st.session_state.affirmation_category == "comfort" else "secondary")
    if comfort_selected:
        change_category("comfort")

with col3:
    growth_selected = st.button("🌱 Growth",
                               key="growth_btn",
                               use_container_width=True,
                               type="primary" if st.session_state.affirmation_category == "growth" else "secondary")
    if growth_selected:
        change_category("growth")



# Display current affirmation with category indicator
category_emoji = "✨" if st.session_state.affirmation_category == "confidence" else "🌈" if st.session_state.affirmation_category == "comfort" else "🌱"
category_name = st.session_state.affirmation_category.capitalize()

st.markdown(f"""
<div class="affirmation-card">
    <div style="position: absolute; top: 10px; left: 10px; background-color: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem;">
        {category_emoji} {category_name}
    </div>
    <p style="font-size: 1.5rem; font-weight: 500; margin-top: 10px;">{st.session_state.current_affirmation}</p>
</div>
""", unsafe_allow_html=True)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    st.button("🔄 New Affirmation", on_click=update_affirmation, use_container_width=True)
with col2:
    st.button("❤ Add to Favorites", on_click=add_to_favorites, use_container_width=True)

# Function to remove from favorites
def remove_from_favorites(index):
    if 0 <= index < len(st.session_state.favorite_affirmations):
        st.session_state.favorite_affirmations.pop(index)
        # Save to file for persistence between sessions
        save_favorites_to_file()

# Display favorites if any
if st.session_state.favorite_affirmations:
    with st.expander("❤ Your Favorite Affirmations"):
        for i, fav in enumerate(st.session_state.favorite_affirmations):
            cols = st.columns([10, 1])
            with cols[0]:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 10px;">
                    <p style="margin: 0; color: #2C3E50;">{fav}</p>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                if st.button("🗑", key=f"remove_{i}", help="Remove from favorites"):
                    remove_from_favorites(i)
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<h3 style="text-align: center; margin-bottom: 20px;">Wellness Resources</h3>', unsafe_allow_html=True)

st.markdown('<p style="text-align: center; margin-bottom: 25px;">How are you feeling today? Select your current state to discover helpful resources.</p>', unsafe_allow_html=True)

# Initialize mood in session state if not exists
if 'resource_mood' not in st.session_state:
    st.session_state.resource_mood = None

# Function to set mood
def set_mood(mood):
    st.session_state.resource_mood = mood

# Mood selection with better UI and icons
st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    sad_card = f"""
    <div style="background: {'linear-gradient(135deg, #3498DB 0%, #2980B9 100%)' if st.session_state.resource_mood == 'sad' else 'white'};
         border-radius: 12px; padding: 20px 15px; text-align: center; cursor: pointer;
         box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;
         color: {'white' if st.session_state.resource_mood == 'sad' else '#2C3E50'};">
        <div style="font-size: 2rem; margin-bottom: 10px;">😢</div>
        <div style="font-weight: 500;">Feeling Sad</div>
    </div>
    """
    if st.markdown(sad_card, unsafe_allow_html=True):
        pass
    sad_selected = st.button("Select", key="sad_btn",
                           use_container_width=True,
                           type="primary" if st.session_state.resource_mood == "sad" else "secondary")
    if sad_selected:
        set_mood("sad")

with col2:
    anxious_card = f"""
    <div style="background: {'linear-gradient(135deg, #3498DB 0%, #2980B9 100%)' if st.session_state.resource_mood == 'anxious' else 'white'};
         border-radius: 12px; padding: 20px 15px; text-align: center; cursor: pointer;
         box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;
         color: {'white' if st.session_state.resource_mood == 'anxious' else '#2C3E50'};">
        <div style="font-size: 2rem; margin-bottom: 10px;">😰</div>
        <div style="font-weight: 500;">Feeling Anxious</div>
    </div>
    """
    if st.markdown(anxious_card, unsafe_allow_html=True):
        pass
    anxious_selected = st.button("Select", key="anxious_btn",
                               use_container_width=True,
                               type="primary" if st.session_state.resource_mood == "anxious" else "secondary")
    if anxious_selected:
        set_mood("anxious")

with col3:
    stressed_card = f"""
    <div style="background: {'linear-gradient(135deg, #3498DB 0%, #2980B9 100%)' if st.session_state.resource_mood == 'stressed' else 'white'};
         border-radius: 12px; padding: 20px 15px; text-align: center; cursor: pointer;
         box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;
         color: {'white' if st.session_state.resource_mood == 'stressed' else '#2C3E50'};">
        <div style="font-size: 2rem; margin-bottom: 10px;">😓</div>
        <div style="font-weight: 500;">Feeling Stressed</div>
    </div>
    """
    if st.markdown(stressed_card, unsafe_allow_html=True):
        pass
    stressed_selected = st.button("Select", key="stressed_btn",
                                use_container_width=True,
                                type="primary" if st.session_state.resource_mood == "stressed" else "secondary")
    if stressed_selected:
        set_mood("stressed")

with col4:
    motivated_card = f"""
    <div style="background: {'linear-gradient(135deg, #3498DB 0%, #2980B9 100%)' if st.session_state.resource_mood == 'motivated' else 'white'};
         border-radius: 12px; padding: 20px 15px; text-align: center; cursor: pointer;
         box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;
         color: {'white' if st.session_state.resource_mood == 'motivated' else '#2C3E50'};">
        <div style="font-size: 2rem; margin-bottom: 10px;">💪</div>
        <div style="font-weight: 500;">Need Motivation</div>
    </div>
    """
    if st.markdown(motivated_card, unsafe_allow_html=True):
        pass
    motivated_selected = st.button("Select", key="motivated_btn",
                                 use_container_width=True,
                                 type="primary" if st.session_state.resource_mood == "motivated" else "secondary")
    if motivated_selected:
        set_mood("motivated")

st.markdown('</div>', unsafe_allow_html=True)

# Display resources based on selection
if st.session_state.resource_mood:
    mood_titles = {
        'sad': 'Resources for When You Feel Sad',
        'anxious': 'Resources for When You Feel Anxious',
        'stressed': 'Resources for When You Feel Stressed',
        'motivated': 'Resources for Motivation & Growth'
    }

    mood_descriptions = {
        'sad': 'These resources can help you understand and process feelings of sadness, find comfort, and discover ways to lift your mood.',
        'anxious': 'These resources offer techniques to manage anxiety, calm your mind, and develop coping strategies for anxious thoughts.',
        'stressed': 'These resources provide methods to reduce stress, relax your body and mind, and build resilience against stressors.',
        'motivated': 'These resources can help you find inspiration, set meaningful goals, and maintain motivation for personal growth.'
    }

    mood_colors = {
        'sad': '#3498DB',
        'anxious': '#3498DB',
        'stressed': '#3498DB',
        'motivated': '#3498DB'
    }

    st.markdown(f'<h4 style="margin-top: 30px; margin-bottom: 10px; color: {mood_colors[st.session_state.resource_mood]};">{mood_titles[st.session_state.resource_mood]}</h4>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin-bottom: 20px; color: #7f8c8d;">{mood_descriptions[st.session_state.resource_mood]}</p>', unsafe_allow_html=True)

    # Create a grid layout for resources
    resource_list = resources[st.session_state.resource_mood]

    # Display resources in a grid
    cols = st.columns(2)
    for i, resource in enumerate(resource_list):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="resource-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex-grow: 1;">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 1.5rem; margin-right: 10px;">{resource['icon']}</span>
                            <div>
                                <h5 style="margin: 0; color: #2C3E50;">{resource['title']}</h5>
                                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #7f8c8d;">{resource['type']}</p>
                            </div>
                        </div>
                    </div>
                    <a href="{resource['url']}" target="_blank" style="background: {mood_colors[st.session_state.resource_mood]}; color: white; padding: 6px 12px; border-radius: 12px; font-size: 0.9rem; text-decoration: none; white-space: nowrap;">View</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown('<p style="text-align: center; margin-top: 30px; color: #7f8c8d; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">Select how you\'re feeling above to see personalized resources that might help.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)