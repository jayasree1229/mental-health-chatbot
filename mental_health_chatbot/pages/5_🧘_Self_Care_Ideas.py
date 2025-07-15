import streamlit as st
import json
import os
import random

# Import necessary modules
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple sidebar
with st.sidebar:
    st.write("Welcome to Mental Health Companion!")

# Function to save self-care plan to a file
def save_selfcare_plan_to_file(plan_items):
    # Create a directory for user data if it doesn't exist
    if not os.path.exists("user_data"):
        os.makedirs("user_data")

    # Create a file path for the guest user
    file_path = "user_data/Guest_selfcare_plan.json"

    # Save the data to the file
    with open(file_path, "w") as f:
        json.dump(plan_items, f)

# Function to load self-care plan from a file
def load_selfcare_plan_from_file():
    file_path = "user_data/Guest_selfcare_plan.json"

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
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid #e6e6e6;
}

/* Self-care category */
.self-care-category {
    background-color: #f8f9fa;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #e6e6e6;
}

/* Self-care item */
.self-care-item {
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
    background-color: #f8f9fa;
}

/* Search box */
.search-container {
    margin-bottom: 20px;
}

/* Quick idea button */
.quick-idea-btn {
    background-color: #3498DB;
    color: white;
    padding: 10px 15px;
    border-radius: 12px;
    text-align: center;
    margin: 10px 0;
    cursor: pointer;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Page title with gradient
st.markdown('<h1 style="background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">Self-Care Ideas by Mood</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 20px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <p style="font-size: 1.1rem;">Different emotional states call for different self-care approaches. Explore these ideas based on how you're feeling.</p>
</div>
""", unsafe_allow_html=True)

# Add custom CSS to make the expanders wider
st.markdown("""
<style>
    /* Make expanders wider */
    .st-emotion-cache-1gulkj5 {
        max-width: 1000px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Make the content inside expanders wider */
    .st-emotion-cache-1d3w5wq {
        width: 100% !important;
        max-width: 1000px !important;
    }
</style>
""", unsafe_allow_html=True)



# Removed search field as requested

# Create a dictionary of all self-care ideas with icons
all_self_care_ideas = {
    "anxious_stressed": {
        "icon": "😌",
        "color": "#9B59B6",
        "ideas": [
            {"title": "Deep breathing", "description": "Try the 4-7-8 technique (inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds). This activates your parasympathetic nervous system, helping to calm your body's stress response."},
            {"title": "Progressive muscle relaxation", "description": "Tense and release each muscle group from your toes to your head. This helps release physical tension that accumulates during stress."},
            {"title": "Grounding exercise", "description": "Practice the 5-4-3-2-1 technique by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. This brings you back to the present moment."},
            {"title": "Limit caffeine and sugar", "description": "Both can increase feelings of anxiety and jitteriness. Try herbal tea or water with lemon instead."},
            {"title": "Go for a walk in nature", "description": "Natural settings help reduce stress hormones and improve mood. Even 15 minutes can make a difference."},
            {"title": "Write down your worries", "description": "Getting thoughts out of your head and onto paper can help you gain perspective and reduce rumination."}
        ]
    },
    "sad_down": {
        "icon": "🌈",
        "color": "#3498DB",
        "ideas": [
            {"title": "Move your body", "description": "Even light exercise releases endorphins that can lift your mood. A short walk, gentle yoga, or dancing to a favorite song can help."},
            {"title": "Reach out to someone", "description": "Share how you're feeling with a trusted friend or family member. Connection can provide comfort and perspective."},
            {"title": "Do something creative", "description": "Engaging in creative activities like drawing, writing, or playing music can help express emotions and shift your focus."},
            {"title": "Practice self-compassion", "description": "Speak to yourself as you would to a friend going through a difficult time. Acknowledge your feelings without judgment."},
            {"title": "Plan something to look forward to", "description": "Even something small like watching a favorite show or ordering a special meal can give you a positive focus."},
            {"title": "Get some sunlight", "description": "Natural light can boost serotonin levels and improve mood. Try to get at least 15 minutes of sunlight exposure daily."}
        ]
    },
    "tired_low_energy": {
        "icon": "⚡",
        "color": "#F39C12",
        "ideas": [
            {"title": "Take a power nap", "description": "A 20-minute nap can restore alertness without interfering with nighttime sleep. Set an alarm to avoid oversleeping."},
            {"title": "Stay hydrated", "description": "Dehydration is a common cause of fatigue. Drink a glass of water and notice if your energy improves."},
            {"title": "Eat energy-boosting foods", "description": "Choose complex carbohydrates paired with protein, like nuts, fruits, and whole grains for sustained energy."},
            {"title": "Try a quick yoga stretch", "description": "Gentle movement increases blood flow and can provide an energy boost. Try a few simple stretches or sun salutations."},
            {"title": "Listen to upbeat music", "description": "Music can naturally energize you and improve your mood. Create a playlist of songs that make you feel good."},
            {"title": "Take a cool shower", "description": "The sensation of cool water can increase alertness and improve circulation."}
        ]
    },
    "overwhelmed": {
        "icon": "🧘",
        "color": "#2ECC71",
        "ideas": [
            {"title": "Break tasks into smaller steps", "description": "Divide large projects into manageable chunks and focus on one step at a time."},
            {"title": "Use the Pomodoro technique", "description": "Work in focused 25-minute intervals followed by 5-minute breaks to maintain productivity without burnout."},
            {"title": "Declutter your physical space", "description": "A tidy environment can help create mental clarity. Start with just one small area if the whole space feels too much."},
            {"title": "Practice saying no", "description": "Set boundaries around new commitments when you're at capacity. It's okay to prioritize your wellbeing."},
            {"title": "Do a brain dump", "description": "Write down everything that's on your mind without organizing it. Then categorize and prioritize once it's all on paper."},
            {"title": "Focus on one thing at a time", "description": "Multitasking increases stress and reduces efficiency. Give your full attention to a single task."}
        ]
    }
}


# Define mood titles for display
mood_titles = {
    "anxious_stressed": "When you're feeling anxious or stressed",
    "sad_down": "When you're feeling sad or down",
    "tired_low_energy": "When you're feeling tired or low energy",
    "overwhelmed": "When you're feeling overwhelmed"
}

# Create expandable sections for different moods with more detailed content
for mood, mood_data in all_self_care_ideas.items():
    # Get the icon and color for this mood
    icon = mood_data["icon"]
    color = mood_data["color"]
    ideas = mood_data["ideas"]

    # Create a custom expander header with icon and color
    expander_label = f"{icon} {mood_titles[mood]}"
    with st.expander(expander_label, expanded=False):
        for i, idea in enumerate(ideas):
            st.markdown(f"""
            <div class="self-care-item" style="border-left: 3px solid {color}; padding-left: 15px; max-width: 900px; margin: 0 auto;">
                <div style="display: block; width: 100%;">
                    <p style="margin-bottom: 8px;"><strong style="color: {color}; font-size: 1.1rem;">{idea["title"]}</strong></p>
                    <p style="margin-top: 0; font-size: 0.95rem; margin-bottom: 0; line-height: 1.5;">{idea["description"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Add a separator between items, except for the last one
            if i < len(ideas) - 1:
                st.markdown('<hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<h2 style="text-align: center; margin-bottom: 10px;">Create Your Personal Self-Care Plan</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; margin-bottom: 25px;">Select activities that resonate with you to build your personalized self-care toolkit.</p>', unsafe_allow_html=True)

# Load saved self-care plan if it exists
if 'selfcare_plan' not in st.session_state:
    st.session_state.selfcare_plan = load_selfcare_plan_from_file()

# Check if we have a new item to add to the plan from the quick add buttons
if 'add_to_plan_item' in st.query_params:
    # Get the item and decode it (it may be URL-encoded)
    new_item = st.query_params['add_to_plan_item']
    try:
        import urllib.parse
        new_item = urllib.parse.unquote(new_item)
    except:
        # If decoding fails, use the original value
        pass

    # Add the item to the plan if it's not already there
    if new_item not in st.session_state.selfcare_plan:
        st.session_state.selfcare_plan.append(new_item)
        # Save the updated plan
        save_selfcare_plan_to_file(st.session_state.selfcare_plan)
        # Show a success message
        st.success(f"Added '{new_item}' to your self-care plan!")

    # Clear the query parameter to prevent adding the same item multiple times
    st.query_params.clear()

# Define self-care categories with icons and colors
selfcare_categories = {
    "physical": {
        "icon": "💪",
        "color": "#3498DB",
        "title": "Physical Self-Care",
        "items": [
            "Regular exercise",
            "Adequate sleep",
            "Healthy eating",
            "Stay hydrated",
            "Take breaks from screens"
        ]
    },
    "emotional": {
        "icon": "❤️",
        "color": "#E74C3C",
        "title": "Emotional Self-Care",
        "items": [
            "Journal about feelings",
            "Practice self-compassion",
            "Allow yourself to cry",
            "Laugh and find humor",
            "Express emotions creatively"
        ]
    },
    "social": {
        "icon": "👥",
        "color": "#9B59B6",
        "title": "Social Self-Care",
        "items": [
            "Connect with friends",
            "Ask for help when needed",
            "Set healthy boundaries",
            "Join a community group",
            "Spend time with supportive people"
        ]
    },
    "spiritual": {
        "icon": "✨",
        "color": "#2ECC71",
        "title": "Spiritual Self-Care",
        "items": [
            "Meditation or mindfulness",
            "Spend time in nature",
            "Practice gratitude",
            "Reflect on personal values",
            "Find meaning in daily activities"
        ]
    }
}


# Initialize checkboxes with saved values
def is_item_in_plan(item):
    return item in st.session_state.selfcare_plan

# Create tabs for each category
tabs = st.tabs([f"{cat_data['icon']} {cat_data['title']}" for cat in selfcare_categories for cat_data in [selfcare_categories[cat]]])

# Dictionary to store checkbox states
checkbox_states = {}

# Populate each tab with its items
for i, (cat, cat_data) in enumerate(selfcare_categories.items()):
    with tabs[i]:
        st.markdown(f"<p style='color: {cat_data['color']}; font-size: 1.1rem; font-weight: 500; margin-bottom: 15px;'>Select the {cat_data['title'].lower()} activities you want to include in your plan:</p>", unsafe_allow_html=True)

        # Create two columns for checkboxes
        col1, col2 = st.columns(2)

        # Distribute items between columns
        half = len(cat_data["items"]) // 2 + len(cat_data["items"]) % 2

        # First column
        with col1:
            for j, item in enumerate(cat_data["items"][:half]):
                key = f"{cat}_{j}"
                checkbox_states[key] = st.checkbox(
                    item,
                    key=key,
                    value=is_item_in_plan(item),
                    label_visibility="visible"
                )

        # Second column
        with col2:
            for j, item in enumerate(cat_data["items"][half:], start=half):
                key = f"{cat}_{j}"
                checkbox_states[key] = st.checkbox(
                    item,
                    key=key,
                    value=is_item_in_plan(item),
                    label_visibility="visible"
                )

# Collect all selected items
selected_items = []
for cat, cat_data in selfcare_categories.items():
    for j, item in enumerate(cat_data["items"]):
        key = f"{cat}_{j}"
        if key in checkbox_states and checkbox_states[key]:
            selected_items.append(item)

# Add buttons for generating and saving the plan
col1, col2 = st.columns([2,2])
with col1:
    preview_btn = st.button("Preview My Plan", use_container_width=True)
with col2:
    save_btn = st.button("Save My Plan", use_container_width=True)

# Display the plan based on button clicks
if save_btn:
    if selected_items:
        st.session_state.selfcare_plan = selected_items
        save_selfcare_plan_to_file(selected_items)
        st.success("Your self-care plan has been saved! It will be available the next time you log in.")

        # Show the saved plan in a nice format
        st.markdown("""
        <div style="background-color: #f0f8ff; border-radius: 15px; padding: 20px; margin-top: 20px; border: 1px solid #d1e6fa;">
            <h3 style="color: #3498DB; margin-bottom: 15px; font-size: 1.3rem;">Your Saved Self-Care Plan</h3>
        """, unsafe_allow_html=True)

        # Group items by category for display
        for cat, cat_data in selfcare_categories.items():
            category_items = [item for item in selected_items if item in cat_data["items"]]
            if category_items:
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <h4 style="color: {cat_data['color']}; margin-bottom: 10px;">{cat_data['icon']} {cat_data['title']}</h4>
                    <ul style="margin-left: 20px;">
                """, unsafe_allow_html=True)

                for item in category_items:
                    st.markdown(f"<li style='margin-bottom: 5px;'>{item}</li>", unsafe_allow_html=True)

                st.markdown("</ul></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please select at least one self-care activity to save your plan.")

# Preview the plan when the preview button is clicked
if preview_btn:
    if selected_items:
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 15px; padding: 20px; margin-top: 20px; border: 1px solid #e6e6e6;">
            <h3 style="color: #3498DB; margin-bottom: 15px; font-size: 1.3rem;">My Self-Care Commitments</h3>
        """, unsafe_allow_html=True)

        # Group items by category for display
        for cat, cat_data in selfcare_categories.items():
            category_items = [item for item in selected_items if item in cat_data["items"]]
            if category_items:
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <h4 style="color: {cat_data['color']}; margin-bottom: 10px;">{cat_data['icon']} {cat_data['title']}</h4>
                    <ul style="margin-left: 20px;">
                """, unsafe_allow_html=True)

                for item in category_items:
                    st.markdown(f"<li style='margin-bottom: 5px;'>{item}</li>", unsafe_allow_html=True)

                st.markdown("</ul></div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e6e6e6;">
                <h4 style="color: #3498DB; margin-bottom: 10px; font-size: 1.2rem;">💡 Tips for Success</h4>
                <ul>
                    <li>Start small with just 1-2 activities and build from there</li>
                    <li>Schedule your self-care activities in your calendar</li>
                    <li>Track your progress and how you feel after each activity</li>
                    <li>Be flexible and adjust your plan as needed</li>
                    <li>Celebrate your commitment to taking care of yourself</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please select at least one self-care activity to preview your plan.")

st.markdown('</div>', unsafe_allow_html=True)


# Add JavaScript to handle adding items to the plan
st.markdown("""
<script>
    // Function to add an item to the self-care plan
    function addToPlan(itemTitle, buttonId) {
        // Change button appearance
        const button = document.getElementById(buttonId);
        button.innerText = 'Added!';
        button.style.backgroundColor = '#2ECC71';

        // Create a URL with the item as a query parameter
        const url = new URL(window.location.href);
        url.searchParams.set('add_to_plan_item', encodeURIComponent(itemTitle));

        // Navigate to the URL with the query parameter
        window.location.href = url.toString();
    }
</script>

<!-- No hidden form needed with query parameter approach -->
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; margin-bottom: 20px; max-width: 1000px; margin-left: auto; margin-right: auto;">Self-Care by Time Commitment</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; margin-bottom: 20px; max-width: 1000px; margin-left: auto; margin-right: auto;">Even when you\'re busy, you can find ways to practice self-care.</p>', unsafe_allow_html=True)

# Add custom CSS to make the time-based expanders wider
st.markdown("""
<style>
    /* Make time-based expanders wider */
    .st-emotion-cache-1gulkj5 {
        max-width: 1000px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# Create a dictionary of time-based self-care ideas
time_based_ideas = {
    "quick": [
        {"title": "Take 5 deep breaths", "description": "Inhale for 4 counts, exhale for 6 counts"},
        {"title": "Stretch at your desk", "description": "Reach arms overhead, roll shoulders, stretch neck"},
        {"title": "Text a friend", "description": "Send a quick message to someone you care about"},
        {"title": "Step outside", "description": "Get some fresh air and sunlight"},
        {"title": "Drink a glass of water", "description": "Stay hydrated for better mood and energy"},
        {"title": "Practice gratitude", "description": "Write down three things you're thankful for"},
        {"title": "Listen to a favorite song", "description": "Music can quickly shift your mood"},
        {"title": "Tidy one small space", "description": "Clear off your desk or a counter"},
        {"title": "Apply hand lotion", "description": "Practice mindfulness while moisturizing"},
        {"title": "Look at nature photos", "description": "Even images of nature can be calming"}
    ],
    "medium": [
        {"title": "Take a short walk", "description": "Even 15 minutes of movement can boost mood"},
        {"title": "Do a guided meditation", "description": "Many apps offer short sessions"},
        {"title": "Journal", "description": "Write about your thoughts and feelings"},
        {"title": "Call a friend", "description": "Connect with someone who lifts your spirits"},
        {"title": "Take a power nap", "description": "20 minutes can restore energy"},
        {"title": "Make a healthy snack", "description": "Nourish your body with something nutritious"},
        {"title": "Do a quick yoga sequence", "description": "Find free videos online"},
        {"title": "Read a chapter of a book", "description": "Escape into another world briefly"},
        {"title": "Take a shower", "description": "Use a special soap or shampoo as a treat"},
        {"title": "Declutter a drawer", "description": "Creating order can calm the mind"}
    ],
    "long": [
        {"title": "Take a long bath", "description": "Add epsom salts, bubbles, or essential oils"},
        {"title": "Prepare a special meal", "description": "Cook something nourishing and delicious"},
        {"title": "Go for a hike", "description": "Spend extended time in nature"},
        {"title": "Watch a movie", "description": "Choose something uplifting or nostalgic"},
        {"title": "Meet a friend for coffee", "description": "Prioritize in-person connection"},
        {"title": "Attend a fitness class", "description": "Move your body in a structured way"},
        {"title": "Create art", "description": "Draw, paint, or craft without judgment"},
        {"title": "Garden", "description": "Connect with nature and create beauty"},
        {"title": "Take a digital detox", "description": "Disconnect from screens for a while"},
        {"title": "Practice a hobby", "description": "Engage in an activity purely for enjoyment"}
    ]
}

# Use expanders instead of tabs to keep content collapsed by default
st.markdown('<h3 style="text-align: center; margin-bottom: 20px; max-width: 1000px; margin-left: auto; margin-right: auto;">Choose a time commitment:</h3>', unsafe_allow_html=True)

# Create expandable sections for different time commitments
for time_key, time_data in time_based_ideas.items():
    # Create labels for each time commitment
    time_labels = {
        "quick": "5 Minutes or Less",
        "medium": "15-30 Minutes",
        "long": "1 Hour or More"
    }

    # Create a custom expander header
    expander_label = f"⏱️ {time_labels[time_key]}"
    with st.expander(expander_label, expanded=False):
        for i, idea in enumerate(time_data):
            st.markdown(f"""
            <div class="self-care-item" style="border-left: 3px solid #3498DB; padding-left: 15px; max-width: 900px; margin: 0 auto;">
                <div style="display: block; width: 100%;">
                    <p style="margin-bottom: 8px;"><strong style="color: #3498DB; font-size: 1.1rem;">{idea["title"]}</strong></p>
                    <p style="margin-top: 0; font-size: 0.95rem; margin-bottom: 0; line-height: 1.5;">{idea["description"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Add a separator between items, except for the last one
            if i < len(time_data) - 1:
                st.markdown('<hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add a footer with a motivational quote
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: #7f8c8d; font-style: italic;">
    "Self-care is not self-indulgence, it is self-preservation." — Audre Lorde
</div>
""", unsafe_allow_html=True)
