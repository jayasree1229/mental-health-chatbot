import streamlit as st
import json
import os

# Set the page title and icon
st.set_page_config(page_title="Mental Health Companion", page_icon="🧠")

# Create user_data directory if it doesn't exist
if not os.path.exists("user_data"):
    os.makedirs("user_data")

# Simple CSS styling
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
    padding: 10px 0;
    margin: 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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

/* Style the app title */
h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #2C3E50 !important;
    margin-bottom: 1.5rem !important;
    margin-top: 1.5rem !important;
    text-align: center !important;
    letter-spacing: -0.5px !important;
    padding-top: 1rem !important;
}

/* Adjust spacing at top */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0 !important;
    max-width: 46rem !important;
}
</style>
""", unsafe_allow_html=True)

# Title Section
st.title("🧠 AI-Powered Mental Health Companion")
st.markdown("""
    Welcome to Your Personal Mental Health Companion
        Here for you, anytime, anywhere. 💬""")

# Main content - styled card with information about the Mental Health Companion
st.markdown("""
    <div style="background-color: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h2 style="color: #2C3E50; margin-bottom: 15px; font-size: 1.5rem;">Your Personal Mental Health Companion</h2>
        <p style="line-height: 1.7; margin-bottom: 15px;">
            Our Mental Health Companion provides a suite of digital tools designed to support your mental wellbeing journey. Through personalized interactions, we offer emotional support, mindfulness techniques, and evidence-based strategies to help manage stress, anxiety, and other mental health concerns.
        </p>
        <p style="line-height: 1.7;">
            With features like mood tracking, guided reflections, and personalized recommendations, we're here to help you build resilience and develop healthy coping mechanisms for everyday challenges.
        </p>
        <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #E0E0E0;">
            <h3 style="color: #3498DB; font-size: 1.2rem; margin-bottom: 10px;">How We Can Help</h3>
            <ul style="padding-left: 20px;">
                <li style="margin-bottom: 8px;">24/7 emotional support through our AI chatbot</li>
                <li style="margin-bottom: 8px;">Daily mood tracking and progress visualization</li>
                <li style="margin-bottom: 8px;">Personalized coping strategies and resources</li>
                <li>Regular positive affirmations and mindfulness exercises</li>
            </ul>
        </div>
    </div>
""", unsafe_allow_html=True)

# Positive Affirmation
st.markdown("Affirmation for today: \n`You are stronger than you think.`")

# Quick Start and Features
st.subheader("How to Start:")
st.markdown("""
- Chat with the AI for emotional support.
- Track your daily mood and see your progress.
- Get daily positive affirmations to uplift your spirit.
""")

# CTA: Start Button
if st.button("Start Your Journey"):
    st.write("Go to the sidebar to start exploring your journey! 🌟")

# Resources Section
st.markdown("""
<div style="margin-top: 20px; padding: 20px; background-color: #f8f9fa; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
    <h4 style="color: #000000; margin-bottom: 15px;">Mental Health Resources</h4>
    <ul>
        <li style="margin-bottom: 12px;"><a href="https://www.nimh.nih.gov" target="_blank" style="color: #3498DB;">National Institute of Mental Health</a> - Evidence-based information on mental health conditions</li>
        <li style="margin-bottom: 12px;"><a href="https://988lifeline.org" target="_blank" style="color: #3498DB;">988 Suicide & Crisis Lifeline</a> - 24/7 support at 988 or 1-800-273-8255</li>
        <li style="margin-bottom: 12px;"><a href="https://www.crisistextline.org" target="_blank" style="color: #3498DB;">Crisis Text Line</a> - Text HOME to 741741 for 24/7 crisis support</li>
        <li style="margin-bottom: 12px;"><a href="https://www.psychologytoday.com/us/therapists" target="_blank" style="color: #3498DB;">Find a Therapist</a> - Search for mental health professionals in your area</li>
        <li style="margin-bottom: 12px;"><a href="https://www.nami.org" target="_blank" style="color: #3498DB;">National Alliance on Mental Illness</a> - Support groups, education, and advocacy</li>
        <li><a href="https://www.headspace.com" target="_blank" style="color: #3498DB;">Headspace</a> - Meditation and mindfulness app with free basic features</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Emergency Help
st.markdown("""
<div style="margin-top: 20px; padding: 15px; background-color: #f8d7da; border-radius: 12px; border-left: 5px solid #dc3545;">
    <h4 style="color: #721c24; margin-bottom: 10px;">Need Immediate Help?</h4>
    <p style="margin-bottom: 10px;">If you're experiencing a mental health crisis or having thoughts of suicide, please reach out for help:</p>
    <ul>
        <li style="margin-bottom: 8px;"><strong>988 Suicide & Crisis Lifeline:</strong> Call or text 988, or chat at <a href="https://988lifeline.org" target="_blank" style="color: #721c24; font-weight: bold;">988lifeline.org</a></li>
        <li style="margin-bottom: 8px;"><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
        <li><strong>Emergency Services:</strong> Call 911 or go to your nearest emergency room</li>
    </ul>
</div>
""", unsafe_allow_html=True)