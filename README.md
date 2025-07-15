
# 🧠 Mental Health Chatbot

This project is a **Mental Health Chatbot** designed to support users in tracking their mood, receiving affirmations, getting wellness tips, and exploring self-care ideas. Built using Python, Streamlit, and various data files, this chatbot serves as a digital mental wellness companion.

---

## 📁 Project Structure

```
mental_health_chatbot/
├── algorithms_summary.md
├── technologies.md
├── mental_health_chatbot/
│   ├── Home.py
│   ├── mental_health_intents.json
│   ├── mental_health_signs.jpg
│   ├── mood_data.csv
│   ├── users.json
│   ├── pages/
│   │   ├── 1_🤖_Chatbot.py
│   │   ├── 2_📅_Daily_CheckIn.py
│   │   ├── 3_💬_Affirmations.py
│   │   ├── 4_📝_Wellness_Tips.py
│   │   └── 5_🧘_Self_Care_Ideas.py
│   ├── static/
│   │   └── js/
│   │       └── tab_switcher.js
│   └── user_data/
│       ├── 1/
│       │   ├── chats.json
│       │   ├── favorites.json
│       │   ├── habits.json
│       │   └── selfcare_plan.json
│       └── Guest/
│           ├── chats.json
│           ├── favorites.json
│           ├── habits.json
│           └── selfcare_plan.json
```

---

## 🚀 Features

- **Interactive Chatbot** powered by predefined intents in JSON format.
- **Daily Mood Check-In** to help track emotional trends.
- **Positive Affirmations** to uplift the user's mindset.
- **Wellness Tips** to encourage mental well-being.
- **Self-Care Ideas** that promote healthy habits.
- **User Data Persistence** through JSON-based storage.
- **Streamlit Interface** for an engaging user experience.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- JSON & CSV for data handling
- JavaScript (for tab switching UI)
- Markdown documentation

---

## 📂 Data Files

- `mental_health_intents.json` – Intent mappings for chatbot conversations.
- `mood_data.csv` – Stores mood tracking data.
- `users.json` – User profile or login data.
- JSON files for storing individual user data such as chats, habits, self-care plans, and favorites.

---

## 📄 Documentation

- `algorithms_summary.md` – Describes the algorithms used in chatbot responses or mood analysis.
- `technologies.md` – Lists the tech stack and their roles in the project.

---

## ▶️ How to Run

1. Make sure you have Python and Streamlit installed:
    ```bash
    pip install streamlit
    ```

2. Navigate to the main project directory:
    ```bash
    cd mental_health_chatbot/mental_health_chatbot/mental_health_chatbot
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run Home.py
    ```

---
