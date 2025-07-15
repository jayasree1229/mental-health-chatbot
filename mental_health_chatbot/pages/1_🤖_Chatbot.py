import streamlit as st
import json
import random
import os
import datetime
import uuid
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Functions to save and load chat history
def save_chat_history(username, messages):
    """Save chat history to a JSON file, keeping only the last 4 chats"""
    # Create user directory if it doesn't exist
    user_dir = f"user_data/{username}"
    os.makedirs(user_dir, exist_ok=True)

    # Generate a title from the first user message
    title = generate_chat_title(messages)

    # Create chat data
    chat_data = {
        "title": title,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": messages
    }

    # Load existing chats
    chats_file = f"{user_dir}/chats.json"
    if os.path.exists(chats_file):
        with open(chats_file, "r") as f:
            try:
                all_chats = json.load(f)
            except json.JSONDecodeError:
                all_chats = []
    else:
        all_chats = []

    # Add new chat to the beginning
    all_chats.insert(0, chat_data)

    # Keep only the last 4 chats
    all_chats = all_chats[:4]

    # Save to file
    with open(chats_file, "w") as f:
        json.dump(all_chats, f)

    return title

def load_chat_histories(username):
    """Load all saved chat histories for a user"""
    chats_file = f"user_data/{username}/chats.json"
    if os.path.exists(chats_file):
        with open(chats_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def generate_chat_title(messages):
    """Generate a title for the chat based on the first user message"""
    if not messages:
        return "New Chat"

    for message in messages:
        if message.get("is_user", False):
            # Use the first 30 characters of the first user message as the title
            title = message["text"][:30]
            if len(message["text"]) > 30:
                title += "..."
            return title

    return "New Chat"
# Import necessary modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple sidebar
with st.sidebar:
    st.write("Welcome to Mental Health Companion!")

# Add JavaScript to check localStorage for chat loading instructions
st.markdown("""
<script>
    // Check if we need to load a chat from localStorage
    document.addEventListener('DOMContentLoaded', function() {
        // Check if we need to load a chat
        const chatIndex = localStorage.getItem("load_chat_index");
        const switchToCurrentChat = localStorage.getItem("switch_to_current_chat");

        if (chatIndex && switchToCurrentChat === "true") {
            console.log("Loading chat index: " + chatIndex);

            // Clear the localStorage values to prevent reloading on refresh
            localStorage.removeItem("load_chat_index");
            localStorage.removeItem("switch_to_current_chat");

            // Create a hidden form to submit the chat index to Streamlit
            const form = document.createElement("form");
            form.style.display = "none";
            form.method = "post";

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "load_chat_index";
            input.value = chatIndex;

            form.appendChild(input);
            document.body.appendChild(form);

            // Submit the form
            form.submit();

            // Find and click the first tab (Current Chat)
            setTimeout(function() {
                const tabs = document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs && tabs.length > 0) {
                    tabs[0].click();
                    console.log("Switched to Current Chat tab");
                }
            }, 500);
        }
    });
</script>
""", unsafe_allow_html=True)

# Custom CSS and JavaScript for styling and functionality
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

/* Chat styling */
.stApp {
    background-color: #f5f7fa;
}

/* Chat messages */
.user-message {
    background: linear-gradient(90deg, #3498DB 0%, #2980B9 100%);
    color: white;
    border-radius: 18px 18px 0 18px;
    padding: 12px 18px;
    margin: 10px 0;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
}

.bot-message {
    background-color: #f1f1f1;
    border-radius: 18px 18px 18px 0;
    padding: 12px 18px;
    margin: 10px 0;
    max-width: 80%;
    margin-right: auto;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Input field styling */
.stTextInput input {
    border-radius: 50px;
    border: 1px solid #E0E0E0;
    padding: 12px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.stTextInput input:focus {
    border-color: #3498DB;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
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

<!-- Include the tab switcher JavaScript -->
<script>
// Function to switch to a specific tab
function switchToTab(tabIndex) {
    // Wait for the DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            performTabSwitch(tabIndex);
        });
    } else {
        // DOM is already ready
        performTabSwitch(tabIndex);
    }
}

// Helper function to perform the actual tab switch
function performTabSwitch(tabIndex) {
    // Add a small delay to ensure the tabs are rendered
    setTimeout(function() {
        const tabs = document.querySelectorAll('[data-baseweb="tab"]');
        if (tabs && tabs.length > tabIndex) {
            tabs[tabIndex].click();
            console.log("Tab switched to index: " + tabIndex);
        } else {
            console.log("Tab not found. Available tabs: " + tabs.length);
        }
    }, 100);
}

// Switch to the first tab (Current Chat)
function switchToCurrentChatTab() {
    switchToTab(0);
}

// Switch to the second tab (Previous Chats)
function switchToPreviousChatsTab() {
    switchToTab(1);
}
</script>
""", unsafe_allow_html=True)

# Streamlit UI with improved design
st.markdown('<h1 style="background: linear-gradient(90deg, #2C3E50 0%, #4CA1AF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; margin-bottom: 1rem;">AI Mental Health Companion</h1>', unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_chat_index' not in st.session_state:
    st.session_state.current_chat_index = -1  # -1 means new chat

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Current Chat"

# Initialize the force_tab_switch flag if it doesn't exist
if 'force_tab_switch' not in st.session_state:
    st.session_state.force_tab_switch = False

# Check if we need to force a tab switch
if st.session_state.force_tab_switch:
    # Reset the flag
    st.session_state.force_tab_switch = False

    # Add JavaScript to force tab switch on page load
    st.markdown("""
    <script>
        // Execute as soon as the DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM loaded, attempting tab switch");

            function switchToFirstTab() {
                // Try multiple selector approaches
                const selectors = [
                    '[data-baseweb="tab"]',
                    '[role="tab"]',
                    '.st-emotion-cache-1avcm0n',
                    '.st-emotion-cache-1avcm0n.e1nzilvr5'
                ];

                for (const selector of selectors) {
                    const tabs = document.querySelectorAll(selector);
                    if (tabs && tabs.length > 0) {
                        console.log(`Found tabs with selector: ${selector}`);
                        tabs[0].click();
                        return true;
                    }
                }

                return false;
            }

            // Try immediately
            if (!switchToFirstTab()) {
                // If not successful, try again after a short delay
                setTimeout(switchToFirstTab, 50);

                // And again after a longer delay as a fallback
                setTimeout(switchToFirstTab, 200);
            }
        });
    </script>
    """, unsafe_allow_html=True)

if 'model' not in st.session_state:
    # Load training data
    import os
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the parent directory
    parent_dir = os.path.dirname(current_dir)
    # Construct the path to the JSON file
    json_path = os.path.join(parent_dir, "mental_health_intents.json")

    with open(json_path) as file:
        data = json.load(file)

    # Prepare training data
    X, y = [], []
    responses = {}

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            X.append(pattern)
            y.append(intent["tag"])
        responses[intent["tag"]] = intent["responses"]

    # Train model
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(X, y)

    # Store in session state
    st.session_state.model = model
    st.session_state.responses = responses

# Function to start a new chat
def start_new_chat():
    st.session_state.chat_history = []
    st.session_state.current_chat_index = -1

# Function to load a previous chat
def load_previous_chat(index):
    chats = load_chat_histories("Guest")
    if 0 <= index < len(chats):
        # Load the messages from the selected chat
        st.session_state.chat_history = chats[index]["messages"]
        # Update the current chat index
        st.session_state.current_chat_index = index
        # Switch to the Current Chat tab
        st.session_state.active_tab = "Current Chat"
        # Set a flag to force tab switching on next run
        st.session_state.force_tab_switch = True

# Add a "New Chat" icon at the top
col1, col2 = st.columns([4, 1])
with col2:
    st.markdown("""
    <style>
    .new-chat-icon {
        background-color: #3498DB;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .new-chat-icon:hover {
        background-color: #2980B9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a clickable icon with a tooltip
    if st.button("➕", help="Start a new chat", key="new_chat_icon"):
        start_new_chat()
        st.rerun()

# Check if we have a form submission with a chat index to load
if 'load_chat_index' in st.query_params:
    try:
        chat_index = int(st.query_params['load_chat_index'])
        # Load the chat
        load_previous_chat(chat_index)
        # Clear the query parameter
        st.query_params.clear()
        # Set the active tab to Current Chat
        st.session_state.active_tab = "Current Chat"
    except (ValueError, TypeError):
        pass

# Create tabs for "Current Chat" and "Previous Chats"
tab_names = ["Current Chat", "Previous Chats"]

# Determine which tab should be active
active_tab_index = 0  # Default to Current Chat
if st.session_state.active_tab == "Previous Chats":
    active_tab_index = 1

# Create a container for the tabs
tab_container = st.container()

# Create the tabs
with tab_container:
    # Create the tabs
    tab1, tab2 = st.tabs(tab_names)

    # Use JavaScript to select the correct tab
    if active_tab_index == 1:  # If Previous Chats should be active
        st.markdown("""
        <script>
            // This script runs after the page loads and selects the Previous Chats tab
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() {
                    const tabs = document.querySelectorAll('[data-baseweb="tab"]');
                    if (tabs && tabs.length > 1) {
                        tabs[1].click();
                        console.log("Switched to Previous Chats tab");
                    }
                }, 100);
            });
        </script>
        """, unsafe_allow_html=True)

# Add a special key to the session state to force a rerun when needed
if 'force_rerun_key' not in st.session_state:
    st.session_state.force_rerun_key = 0

# Function to handle tab change
def handle_tab_change(tab_name):
    st.session_state.active_tab = tab_name

with tab1:
    # Display current chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['is_user']:
                st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 30px; color: #7f8c8d;">
            <p>Start a new conversation with the AI Mental Health Companion.</p>
            <p>Type your message below to begin.</p>
        </div>
        """, unsafe_allow_html=True)

    # Create a form for the chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input("Type your message here...", key="message_input", label_visibility="collapsed")

        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)

        if submit_button and user_input.strip():
            # Add user message to chat history
            st.session_state.chat_history.append({"is_user": True, "text": user_input})

            # Get bot response
            predicted_tag = st.session_state.model.predict([user_input])[0]
            response = random.choice(st.session_state.responses[predicted_tag])

            # Add bot response to chat history
            st.session_state.chat_history.append({"is_user": False, "text": response})

            # Save chat history if there are messages
            if len(st.session_state.chat_history) > 0:
                save_chat_history("Guest", st.session_state.chat_history)

            # Rerun to update the chat display
            st.rerun()

with tab2:
    # Load previous chats
    previous_chats = load_chat_histories("Guest")

    if previous_chats:
        st.markdown("<h3>Your Previous Conversations</h3>", unsafe_allow_html=True)

        for i, chat in enumerate(previous_chats):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 10px; border-radius: 8px; background-color: {'#E6F2FF' if i == st.session_state.current_chat_index else 'white'};">
                    <p style="margin: 0; font-weight: 500;">{chat['title']}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #7f8c8d;">{chat['timestamp']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Center the button
                st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)

                # Use a regular Streamlit button with a key
                if st.button("📂", key=f"load_chat_{i}", help="Load this conversation"):
                    # Load the chat
                    load_previous_chat(i)

                    # Set the active tab to Current Chat
                    st.session_state.active_tab = "Current Chat"

                    # Force a rerun to update the UI
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 30px; color: #7f8c8d;">
            <p>No previous conversations found.</p>
            <p>Start chatting to save your conversations!</p>
        </div>
        """, unsafe_allow_html=True)

# Additional information sections
st.markdown("""
### About This Chatbot

This AI companion is designed to provide emotional support and guidance. It can help with:

- Answering questions about mental health topics
- Providing coping strategies for stress, anxiety, and low mood
- Offering relaxation techniques and mindfulness exercises
- Suggesting self-care activities and healthy habits
- Providing encouragement and motivation

While it can offer helpful responses, it's not a replacement for professional mental health services.

### How to Use the Chatbot

- Type your questions or concerns in the text box above
- Be specific about how you're feeling or what you need help with
- Try phrases like "I'm feeling anxious" or "How can I improve my sleep?"
- The chatbot will respond with supportive messages and practical advice
- Your last 4 conversations are automatically saved for future reference
- Use the "Previous Chats" tab to access your saved conversations
- Click the ➕ icon to start a fresh conversation
- Click the 📂 icon to load a previous conversation
""")

# Add a divider
st.markdown("---")