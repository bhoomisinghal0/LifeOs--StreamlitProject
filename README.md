<div align="center">

# 🧠 Life-OS
### *AI Powered Digital Wellbeing Dashboard*

<img src="screenshots/dashboard.png" width="900"/>

### 🚀 Reclaim your time, one mindful day at a time.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)]()
[![Gemini](https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge&logo=google)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

---

# 📖 About the Project

Life-OS is an **AI-powered Digital Wellbeing Dashboard** built using **Streamlit**, **Pandas**, and an **OpenRouter-hosted Gemini model**.

It analyzes a user's daily screen time habits, visualizes usage trends, generates personalized productivity coaching, and even creates an AI-generated digital avatar representing the user's digital lifestyle.

This project was developed as part of the **MirAI School of Technology – AI Builder Virtual Summer Internship 2026**.

---


# 🏗️ System Architecture

Life-OS follows a simple data-to-insight pipeline:

**Screen-Time Data → Pandas Processing → KPI & Analytics → AI Coach → Structured JSON → Visual Insights**

<img src="docs/System_architecture.png" width="1000"/>
---

# ✨ Features

## 📊 Smart Dashboard

- Daily screen-time tracking
- Interactive date selection
- Custom daily screen-time goal
- KPI cards with goal comparison
- 14-Day screen-time trend visualization
- Interactive screen-time data editor
- Session-based data updates

---

## 🤖 AI Wellbeing Coach

Powered by an **OpenRouter-hosted Gemini model**

The AI:

- Analyzes daily screen-time categories
- Identifies usage patterns
- Detects areas requiring attention
- Appreciates productive coding and educational usage
- Suggests practical offline alternatives
- Provides personalized recommendations
- Generates a daily challenge
- Produces a structured JSON-based coaching response
- Accepts personalized user questions
---

## 🎭 AI Digital Avatar

Life-OS generates a personalized avatar concept based on the user's daily digital habits.

The avatar can represent different digital lifestyle patterns, such as:

🧟 Doomscroll Zombie

😴 Distracted Student

🛡️ Focus Warrior

Images are generated dynamically using **Pollinations AI**.

Avatar generation is handled gracefully so that an avatar failure does not break the main dashboard.

---

## 📝 Interactive Data Editor

Life-OS includes an interactive screen-time data table using Streamlit's `st.data_editor`.

Users can:

- View screen-time records
- Edit data interactively
- Save changes for the current session
- Automatically refresh dashboard calculations after saving

## 🔗 Shareable Accountability Link

Uses Streamlit Query Parameters.

Share your daily screen-time results through the URL with friends or accountability partners.

Example:

```
...?date=2026-08-02&screen_time=340
```

---

## 🎨 Modern UI

- Neon glassmorphism theme
- Animated KPI cards
- Responsive layout
- Sidebar navigation
- Dark futuristic interface

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application logic |
| Streamlit | Dashboard and UI |
| Pandas | Data processing and analysis |
| OpenRouter API | AI model access |
| Gemini 2.5 Flash | AI reasoning and coaching |
| Pollinations AI | AI avatar generation |
| HTML + CSS | Custom UI styling |
| Streamlit Session State | State persistence |

---

# 🧠 Key Implementation Highlights

### Session State Management

`st.session_state` is used to preserve:

- Selected date
- Daily goal
- AI coaching response
- AI avatar state
- Edited screen-time data

### Structured AI Responses

The AI Coach is instructed to return structured JSON containing:

- Verdict
- Patterns
- Main issue
- Recommended actions
- Today's challenge
- Scorecard

The JSON is parsed in Python and transformed into the dashboard's visual coaching interface.

### Graceful Error Handling

AI and avatar generation failures are handled without allowing the entire dashboard to crash.

---
# 📸 Screenshots

## Dashboard

<img src="screenshots/dashboard.png" width="900"/>

---

## AI Coach

<img src="screenshots/coach.png" width="900"/>

---

## Digital Avatar

<img src="screenshots/avatar.png" width="500"/>

---

## KPI Dashboard

<img src="screenshots/kpi.png" width="900"/>

---

## Analytics

<img src="screenshots/graph.png" width="900"/>

---

# 📂 Project Structure

```text
Life-OS/
│
├── app.py
├── style.css
├── screentime.csv
├── requirements.txt
├── .gitignore
├── README.md
│
├── docs/
│   └── System_architecture.png
│
├── screenshots/
│   ├── dashboard.png
│   ├── coach.png
│   ├── avatar.png
│   ├── kpi.png
│   └── graph.png
│
└── .env
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/bhoomisinghal0/LifeOs--StreamlitProject
```

Go inside the folder

```bash
cd Life-OS
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

Run the app

```bash
streamlit run app.py
```

---

# 🌐 Live Demo

🔗 **Live Application**

> https://lifeos--appproject.streamlit.app/?screen_time=795&date=2026-07-18

---

# 💻 GitHub Repository

🔗 https://github.com/bhoomisinghal0/LifeOs--StreamlitProject

---

# 🎯 Future Improvements

- 🎤 Voice Journal
- 📱 Real Screen-Time API Integration
- 📅 Weekly Habit Reports
- 📈 Productivity Score
- 🏆 Achievement Badges

---

# 👨‍💻 Developer

**Bhoomi Singhal**

B.Tech CSE Student

MirAI School of Technology – AI Builder Internship 2026

LinkedIn: *https://www.linkedin.com/in/bhoomi-singhal-a558a736b/*

GitHub: *https://github.com/bhoomisinghal0*

---

<div align="center">

### ⭐ If you like this project, consider giving it a star!

Made with ❤️ using Streamlit, Pandas & AI

</div>