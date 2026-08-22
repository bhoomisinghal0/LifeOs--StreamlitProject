import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
from zoneinfo import ZoneInfo #for india zone timing
import json
import base64 #binary to text ,, text to binary
import urllib.parse  # help in building pollination url
from pathlib import Path #for linking css file

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)
st.set_page_config(page_title="Life-OS", page_icon="🧠", layout="wide")

css_path = Path(__file__).parent / "style.css"

with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

df = pd.read_csv("screentime.csv")
#initializing st.session_state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "selected_day" not in st.session_state:
    st.session_state.selected_day= df["Date"].iloc[0]
if "goal" not in st.session_state:
    st.session_state.goal=240
if"ai_advice_data" not in st.session_state:
    st.session_state.ai_advice_data=None
if "avatar_day" not in st.session_state:
    st.session_state.avatar_day = None
if "avatar_url" not in st.session_state:
    st.session_state.avatar_url = None
if "edited_df" not in st.session_state:
    st.session_state.edited_df = df.copy()
# Always use the current session data
df = st.session_state.edited_df.copy()


def show_signup():

    st.title("🧠 Welcome to Life-OS")

    st.write("Let's personalize your digital wellbeing dashboard.")

    with st.form("signup_form"):

        name = st.text_input("Your Name")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Create My Life-OS")

        if submitted:

            if name.strip() and email.strip():

                st.session_state.user_name = name.strip()

                st.rerun()

            else:
                st.warning("Please fill in all fields.")

if st.session_state.user_name is None:

    show_signup()

else:
    #SIDEBAR 

    st.sidebar.header("Controls 🕹️")


    dates = sorted(df["Date"].unique())
    default_index = 0

    if "imported_date" in st.session_state:
        if st.session_state.imported_date in dates:
            default_index = dates.index(
                st.session_state.imported_date
            )

    selected_day = st.sidebar.selectbox(
        "Select Date",
        dates,
        index=default_index
    )

    goal = st.sidebar.slider(
        "Daily Goal (in minutes)",
        20,  # min value
        600,  # max value
        step=10,
        key="goal"
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
        <h5 style="
            font-size:18px;
            font-weight:900;
            margin-bottom:-20px;
            margin-top: -20px;
            color:#ffffff;
            text-shadow:
            0 0 8px #b5179e,
            0 0 18px #7209b7;
        ">
        📂 Navigation
        </h5>
        """,
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Overview",
            "🎭 Avatar Companion",
            "📊 Performance",
            "📈 Analytics",
            "🤖 AI Coach & Advance Features",
        ],
        label_visibility="collapsed"
    )


    today_df = st.session_state.edited_df[st.session_state.edited_df["Date"] == selected_day].reset_index(
        drop=True
    )  # Reset the index and discard the old one.
    # stores the row which meet the condition and return True

    summary = today_df.groupby("Category")["Minutes_Used"].sum()

    summary_text = summary.to_string()

    total_minutes = today_df["Minutes_Used"].sum()  # total screen time
    st.query_params["screen_time"] = total_minutes
    st.query_params["date"] = selected_day
    params = st.query_params

    shared_time = params.get("screen_time")

    shared_date = params.get("date")
    top_app = today_df.groupby("App_Name")["Minutes_Used"].sum().idxmax()
    
    delta = goal - total_minutes

    def welcome():
        # ---------- WELCOME SECTION ----------
             
        st.markdown(
        '<div class="lifeos-title">🧠 Life-OS Dashboard</div>',
        unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-subtitle">
                🔮 AI Powered Digital Wellbeing Dashboard
            </div>

            <div class="hero-tagline">
                Reclaim your time, one mindful day at a time.
            </div>
            """,
            unsafe_allow_html=True,
        )

        current_hour = datetime.now(ZoneInfo("Asia/Kolkata")).hour

        if current_hour < 12:
            greeting = "Good morning"
        elif current_hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        # Change this later to the name from your signup form
        user_name = st.session_state.get("user_name", "User")

        st.markdown(
        f"""<div class="welcome-card">
        <div class="welcome-content">
        <h2>{greeting}, {user_name} 👋</h2>
        <p>Here's your Life-OS overview for today.</p>
        </div>
        <div class="usage-badge">
        <div class="usage-icon">◷</div>
        <div class="usage-number">{total_minutes}</div>
        <div class="usage-unit">min</div>
        <div class="usage-label">Today's Usage</div>
        </div>
        </div>""",
        unsafe_allow_html=True
        )

        st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
        st.divider()



    def show_usage():

        coln1, coln2 = st.columns(2)
        with coln1:
            st.subheader("📋 Usage")

            if shared_time:

                st.success(f"📢 Shared Screen Time : {shared_time} minutes")
            elif shared_date:
                st.success(f"📢 Shared Date : {shared_date}")

            st.info("Copy the browser URL and send it to your accountability partner.")

            share_url = (
                f"https://lifeos--appproject.streamlit.app/"
                f"?screen_time={total_minutes}&date={selected_day}"
            )

            st.text_input("Shareable Link", share_url)

            with st.expander("📋 View Data"):
                st.dataframe(today_df)


        #to check if new avatar required to create so as API does not exhaust
                    
        needs_new_avatar = (
        st.session_state.avatar_url is None
        or st.session_state.avatar_day != selected_day
        )

        if needs_new_avatar:
            try:
                if total_minutes <= goal :
                    

                    avatar_ai_prompt = f"""
                    Create ONE highly detailed cinematic image-generation prompt.

                    Create a powerful superhero-style warrior standing confidently in a beautiful
                    natural environment filled with colorful flowers, lush green plants and
                    peaceful scenery.

                    The warrior should look strong, heroic, disciplined and balanced, wearing
                    detailed fantasy-inspired superhero armor with elegant metallic textures and
                    subtle glowing elements. Give the warrior a confident but peaceful expression
                    and a powerful heroic stance.

                    Surround the warrior with blooming flowers, green fields, tall trees,
                    mountains in the distance, butterflies and warm golden sunlight filtering
                    through the environment. Add subtle magical particles and a soft atmospheric
                    glow to make the scene feel inspirational and extraordinary.

                    Use cinematic lighting, dramatic perspective, realistic textures, depth of
                    field, wide-angle composition and professional high-detail fantasy
                    concept-art quality.

                    The overall feeling should be peaceful, victorious, powerful and connected
                    with nature.

                    No text, no captions, no logos, no UI, no statistics and no multiple scenes.

                    Return ONLY the final image-generation prompt.
                    Maximum 150 words.
                    """

                elif total_minutes > goal :

                    avatar_ai_prompt = f"""
                    Create ONE highly detailed cinematic image-generation prompt.

                    MAIN SUBJECT:
                    A terrifying but visually interesting zombie sitting and mindlessly scrolling
                    on a smartphone.

                    IMPORTANT COMPOSITION:
                    The smartphone MUST be clearly visible in the zombie's hands and MUST be one
                    of the two main focal points of the image. Show the zombie looking directly at
                    the smartphone screen while actively scrolling with one finger. The phone
                    screen should be large, bright and clearly recognizable.

                    CHARACTER:
                    Show a zombie with pale decayed skin, messy hair, hollow tired eyes and a
                    slouched posture. Its face should be illuminated by the bright blue glow
                    coming directly from the smartphone screen.

                    ENVIRONMENT:
                    Place the zombie in a dark, slightly chaotic environment with scattered
                    objects, eerie atmosphere and atmospheric fog. The glowing smartphone should
                    create a strong pool of blue light around the zombie.

                    VISUAL STYLE:
                    Dramatic cinematic lighting, strong shadows, detailed textures, atmospheric
                    fog, realistic depth of field, dynamic camera composition and professional
                    dark-fantasy digital-art quality.

                    The zombie's hands, smartphone and glowing screen must be clearly visible.
                    Do NOT hide, remove, obscure or replace the smartphone.

                    No text, captions, logos, UI, statistics or multiple scenes.

                    Return ONLY the final image-generation prompt.
                    Maximum 150 words.
                    """
                try:
                    avatar_response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    messages=[{"role": "user", "content": avatar_ai_prompt}],
                    max_tokens=500
                    )

                    avatar_prompt = avatar_response.choices[0].message.content.strip()
                    encoded_prompt = urllib.parse.quote(avatar_prompt)

                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

                    #saving avatar url 
                    st.session_state.avatar_url = image_url
                    st.session_state.avatar_day = selected_day

                except Exception:
                    st.toast("Avatar Can't be generated due to a technical issue")

            except Exception:
                st.toast("Avatar Can't be generated due to a technical issue")

        if st.session_state.avatar_url is not None:
            with coln2:

                colm1, colm2, colm3 = st.columns([1, 8, 1])


                with colm2:
                    st.subheader("🎭 Life-OS Companion")
                    try:
                        st.image(st.session_state.avatar_url, width=220)
                        if total_minutes > goal + 180:

                            caption = "🧟 Doomscroll Zombie"

                            message = "Take a walk without your phone."

                        elif total_minutes > goal:

                            caption = "😴 Distracted Student"

                            message = "Reduce social media by 30 minutes."

                        else:

                            caption = "🛡️ Focus Warrior"

                            message = "Excellent balance today!"

                        st.success(caption)

                        st.caption(message)
                    except Exception:
                        st.toast("Avatar Can't be generated")


        st.divider()


    def show_kpi():
        st.header("Your Key Performance:")

        # creating columns
        col1, col2, col3 = st.columns(3)

        # First KPI

        with col1:
            st.metric(
                label="📱 Today's Screen Time",
                value=f"{total_minutes} min",
                delta="Increased" if total_minutes > goal else "Decreased",
                delta_color="inverse" if total_minutes > goal else "normal",
            )

        # Second KPI

        with col2:
            st.metric(
                label="🏆 Most Used App",
                value=top_app,
                delta=f"Control on Usage",
                delta_color="inverse",
            )

        # Third KPI

        with col3:
            st.metric(
                label="🎯 Goal Difference",
                value=f"✅{abs(delta)} min" if delta >= 0 else f"⚠️{abs(delta)} min",
                delta=f"{delta} min",
            )

        st.divider()
    def edit():
        st.subheader("📝 Screen-Time Data")

        edited_df = st.data_editor(
            df,
            width= 'stretch',
            hide_index=True,
        )

        if st.button("💾 Save Changes"):
            st.session_state.edited_df = edited_df.copy()
            st.rerun()
            st.success("Screen-time data updated for this session.")


    def show_graph():
        st.subheader("14 Days Screen-Time Trend")
        trend = df.groupby("Date")["Minutes_Used"].sum()
        st.line_chart(trend, height=350)
        st.divider()


    def show_ai():

        system_prompt = f"""
        You are Life-OS AI, a personalized digital wellbeing coach.

        Your job is to analyze the user's screen-time habits and provide
        practical, realistic, and personalized digital wellbeing guidance.

        Follow these rules:
        - Base your analysis only on the data provided by the application.
        - Never invent screen-time numbers.
        - Treat coding and educational screen time as potentially productive.
        - Never recommend reducing coding time when it is being used productively.
        - If Social Media usage is high, suggest practical offline alternatives.
        - If Entertainment usage is high, suggest healthier leisure alternatives.
        - Keep recommendations concise and achievable.
        - Return the requested information in valid JSON only.
        """
        prompt= f"""
            Analyze the user's current screen-time data.

            Today's screen-time data:
            {summary_text}

            Daily goal: {goal} minutes
            Actual screen time: {total_minutes} minutes

            Return exactly the JSON structure requested below.

            {{
                "verdict": {{
                    "status": "GOOD or NEEDS_ATTENTION",
                    "title": "short title",
                    "summary": "one short sentence"
                }},

                "snapshot": {{
                    "total_minutes": {total_minutes},
                    "goal_minutes": {goal},
                    "difference_minutes": {total_minutes - goal}
                }},

                "patterns": [
                    {{
                        "title": "short pattern",
                        "description": "short explanation"
                    }}
                ],

                "main_issue": {{
                    "title": "main issue",
                    "why": "short explanation"
                }},

                "actions": [
                    {{
                        "title": "action 1",
                        "description": "practical suggestion",
                        "priority": "HIGH"
                    }},
                    {{
                        "title": "action 2",
                        "description": "practical suggestion",
                        "priority": "MEDIUM"
                    }},
                    {{
                        "title": "action 3",
                        "description": "practical suggestion",
                        "priority": "MEDIUM"
                    }}
                ],

                "today_challenge": {{
                    "title": "small challenge",
                    "description": "one achievable action"
                }},

                "scorecard": {{
                    "strength": "one short line",
                    "attention": "one short line",
                    "next_step": "one short line"
                }}
            }}

            Rules:

            - Use only the supplied screen-time data.
            - Never invent screen-time numbers.
            - If Coding is high, appreciate productive coding work.
            - Never recommend reducing coding time.
            - If Social Media is high, suggest practical offline alternatives.
            - If Entertainment is high, recommend healthier leisure alternatives.
            - Keep every explanation concise.
            - Give realistic suggestions.
            """

        if st.button("🤖 Get AI Advice"):
            try:
                with st.spinner("Analyzing your digital habits...🤖"):
                    response = client.chat.completions.create(
                        model="google/gemini-2.5-flash",
                        messages=[{
                                        "role": "system",
                                        "content": system_prompt
                                    },
                                    {
                                        "role": "user",
                                        "content": prompt
                                }],
                        max_tokens=1000
                        )

                    raw_response = response.choices[0].message.content

                    # Remove Markdown code fences if the AI adds them
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    elif raw_response.startswith("```"):
                        raw_response = raw_response[3:]

                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    raw_response = raw_response.strip()
                    
                    try:
                        advice_data = json.loads(raw_response)
                    except json.JSONDecodeError:
                        st.warning("The AI returned an unexpected response. Please try again.")
                        advice_data = None

                    if advice_data is not None:
                        st.session_state.ai_advice_data = advice_data
                        verdict = advice_data["verdict"]
                        st.subheader("🎯 Today's Digital Wellbeing Verdict")

                        st.write(f"### {verdict['title']}")
                        st.write(verdict["summary"])

                        #adding pattern
                        st.subheader("🔍 What Your Habits Show")

                        for pattern in advice_data["patterns"]:
                            st.write(f"**{pattern['title']}**")
                            st.write(pattern["description"])

                        #action plan
                        st.subheader("💡 Your Action Plan")
                        actions = advice_data["actions"]

                        action_cols = st.columns(len(actions))

                        for col, action in zip(action_cols, actions):
                            with col:
                                st.markdown(f"### {action['title']}")
                                st.write(action["description"])
                                st.caption(f"Priority: {action['priority']}")

                        main_issue = advice_data["main_issue"]

                        st.subheader("🚨 Main Thing to Watch")

                        st.write(f"### {main_issue['title']}")
                        st.write(main_issue["why"])

                        challenge = advice_data["today_challenge"]

                        st.subheader("🎯 Today's Challenge")

                        st.write(f"### {challenge['title']}")
                        st.write(challenge["description"])

                        scorecard = advice_data["scorecard"]
                        score_cols = st.columns(3)

                        with score_cols[0]:
                            st.subheader("💪 Strength")
                            st.write(scorecard["strength"])

                        with score_cols[1]:
                            st.subheader("👀 Attention")
                            st.write(scorecard["attention"])

                        with score_cols[2]:
                            st.subheader("🚀 Next Step")
                            st.write(scorecard["next_step"])
                            
                        #st.json(advice_data) for debugging
                        st.success("AI advice generated successfully.")
            except Exception as e:
                st.toast("Unable to generate AI advice.")

        st.write("Want more personalized advice based on your screen-time habits? then ask below")
        #AI Coach Form 
        with st.form("AI Coach Form 🤖 "):
            user_context = st.text_area(
                "Ask more that you want your AI coach to consider:",
                placeholder=" type your query",
                height=100
            )
            submitted = st.form_submit_button(
                "Ask AI"
            )

        if submitted:
            try:
                with st.spinner("Analyzing your digital habits... 🤖"):

                    response = client.chat.completions.create(
                        model="google/gemini-2.5-flash",
                        messages=[
                                        {
                                            "role": "system",
                                            "content": system_prompt
                                        },
                                        {
                                            "role": "user",
                                            "content": prompt + f"""
                                            
                                USER'S SPECIFIC QUESTION:
                                {user_context}

                                Answer this specific question using the same JSON structure requested above.
                                """
                                        }
                                    ],
                        max_tokens=1000
                    )

                    raw_response = response.choices[0].message.content

                    # Remove Markdown code fences if the AI adds them
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    elif raw_response.startswith("```"):
                        raw_response = raw_response[3:]

                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]
                    try:
                        advice_data = json.loads(raw_response)
                    except json.JSONDecodeError:
                        st.warning("The AI returned an unexpected response. Please try again.")
                        advice_data = None

                    if advice_data is not None:
                        st.session_state.ai_advice_data = advice_data
                        verdict = advice_data["verdict"]
                        st.subheader("🎯 Today's Digital Wellbeing Verdict")

                        st.write(f"### {verdict['title']}")
                        st.write(verdict["summary"])
                        #adding pattern
                        st.subheader("🔍 What Your Habits Show")

                        for pattern in advice_data["patterns"]:
                            st.write(f"**{pattern['title']}**")
                            st.write(pattern["description"])

                        #action plan
                        st.subheader("💡 Your Action Plan")
                        actions = advice_data["actions"]

                        action_cols = st.columns(len(actions))

                        for col, action in zip(action_cols, actions):
                            with col:
                                st.markdown(f"### {action['title']}")
                                st.write(action["description"])
                                st.caption(f"Priority: {action['priority']}")

                        main_issue = advice_data["main_issue"]

                        st.subheader("🚨 Main Thing to Watch")

                        st.write(f"### {main_issue['title']}")
                        st.write(main_issue["why"])

                        challenge = advice_data["today_challenge"]

                        st.subheader("🎯 Today's Challenge")

                        st.write(f"### {challenge['title']}")
                        st.write(challenge["description"])

                        scorecard = advice_data["scorecard"]
                        score_cols = st.columns(3)

                        with score_cols[0]:
                            st.subheader("💪 Strength")
                            st.write(scorecard["strength"])

                        with score_cols[1]:
                            st.subheader("👀 Attention")
                            st.write(scorecard["attention"])

                        with score_cols[2]:
                            st.subheader("🚀 Next Step")
                            st.write(scorecard["next_step"])
                        #st.json(advice_data) for debugging
                        st.success("AI advice generated successfully.")
            except Exception:
                st.warning(
                    "🤖 AI Coach is temporarily unavailable. "
                    "Your dashboard is still working normally."
                )
        st.divider()
        screen_time_image = import_screen_time_from_image()

    def import_screen_time_from_image():

        st.markdown(
            """
            <div class="ai-section-title">
                <div>
                    <h2>Import Screen Time 📸</h2>
                    <p>Capture or upload your screen-time settings to create a new day.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        camera_col, upload_col = st.columns(2, gap="medium")

        with camera_col:
            st.markdown(
                '<div class="input-label">Take a screen-time screenshot</div>',
                unsafe_allow_html=True
            )

            camera_image = st.camera_input(
                "Take Photo",
                label_visibility="collapsed"
            )

        with upload_col:
            st.markdown(
                '<div class="input-label">Or upload a screen-time screenshot</div>',
                unsafe_allow_html=True
            )

            uploaded_image = st.file_uploader(
                "Upload Screenshot",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed"
            )

        screen_time_image = camera_image or uploaded_image

        if screen_time_image:
            st.divider()
            st.subheader("Uploaded Screenshot Preview")
            st.image(
                screen_time_image,
                caption="Screen-time screenshot",
                width=350
            )

            if st.button("🔍 Analyze Screenshot", key="analyze_screen_time"):

                with st.spinner("Reading your screen-time screenshot... 🤖"):

                    try:
                        # Read image bytes
                        image_bytes = screen_time_image.getvalue()

                        # Convert image to base64 string to embed in api
                        image_base64 = base64.b64encode(
                            image_bytes
                        ).decode("utf-8")

                        # Detect image type
                        mime_type = screen_time_image.type

                        # Gemini vision prompt
                        vision_prompt = """
            You are the Life-OS Screen-Time Data Extractor.

            Analyze the provided screen-time settings screenshot.

            Extract only information that is clearly visible in the screenshot.

            Return ONLY valid JSON.
            Do not use Markdown.
            Do not use ```json.
            Do not add explanations outside the JSON.

            Return exactly this structure:

            {
                "date": "YYYY-MM-DD or null",
                "apps": [
                    {
                        "app_name": "string",
                        "category": "Social Media | Education | Entertainment | Coding | Other",
                        "minutes_used": 0
                    }
                ]
            }

            Rules:

            - Extract every clearly visible app with its screen-time duration.
            - Convert hours and minutes into total minutes.
            - Example: 2h 30m = 150 minutes.
            - Do not invent apps or usage times.
            - If the date is not visible, return null.
            - If an app category is unclear, use "Other".
            - minutes_used must be an integer.
            """

                        response = client.chat.completions.create(
                            model="google/gemini-2.5-flash",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a precise screen-time "
                                        "data extraction engine for Life-OS."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": vision_prompt
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": (
                                                    f"data:{mime_type};"
                                                    f"base64,{image_base64}"
                                                )
                                            }
                                        }
                                    ]
                                }
                            ],
                            max_tokens=1000
                        )

                        raw_response = (
                            response.choices[0].message.content.strip()
                        )

                        # Remove Markdown code fences if Gemini adds them
                        if raw_response.startswith("```json"):
                            raw_response = raw_response[7:]
                        elif raw_response.startswith("```"):
                            raw_response = raw_response[3:]

                        if raw_response.endswith("```"):
                            raw_response = raw_response[:-3]

                        raw_response = raw_response.strip()

                        extracted_data = json.loads(raw_response)

                        #VALIDATE EXTRACTED DATA

                        if not isinstance(extracted_data, dict):
                            raise ValueError("Gemini response is not a JSON object.")

                        if "apps" not in extracted_data:
                            raise ValueError("Gemini response is missing the apps field.")

                        if not isinstance(extracted_data["apps"], list):
                            raise ValueError("Apps data is not in the expected format.")

                        valid_apps = []

                        for app in extracted_data["apps"]:

                            if not isinstance(app, dict):
                                continue

                            app_name = app.get("app_name")
                            category = app.get("category")
                            minutes = app.get("minutes_used")

                            if not app_name:
                                continue

                            if category not in [
                                "Social Media",
                                "Education",
                                "Entertainment",
                                "Coding",
                                "Other"
                            ]:
                                category = "Other"

                            try:
                                minutes = int(minutes)
                            except (TypeError, ValueError):
                                continue

                            if minutes < 0:
                                continue

                            valid_apps.append({
                                "app_name": app_name,
                                "category": category,
                                "minutes_used": minutes
                            })

                        if not valid_apps:
                            raise ValueError(
                                "No valid screen-time apps were found in the screenshot."
                            )

                        extracted_data["apps"] = valid_apps

                        st.session_state.extracted_screen_time = extracted_data

                        st.success(
                            "Screenshot analyzed successfully! Please review the data below. ✅"
                        )
        
                    except json.JSONDecodeError:
                        st.error(
                            "Gemini returned an invalid data format. "
                            "Please try the screenshot again."
                        )

                    except Exception as e:
                        st.error(
                            f"Unable to analyze the screenshot: {e}"
                        )
        # REVIEW EXTRACTED DATA

        if "extracted_screen_time" in st.session_state:

            extracted_data = st.session_state.extracted_screen_time

            st.markdown("### 📋 Review Extracted Screen-Time Data")

            review_df = pd.DataFrame(
                extracted_data["apps"]
            )

            review_df = review_df.rename(
                columns={
                    "app_name": "App",
                    "category": "Category",
                    "minutes_used": "Minutes Used"
                }
            )
            # IMPORT DATE

            default_import_date = extracted_data.get("date")

            try:
                if default_import_date:
                    import_date = datetime.strptime(
                        default_import_date,
                        "%Y-%m-%d"
                    ).date()
                else:
                    import_date = datetime.today().date()
            except (ValueError, TypeError):
                import_date = datetime.today().date()

            import_date = st.date_input(
                "📅 Date for this screen-time data",
                value=import_date,
                key="screen_time_import_date"
            )

            edited_review_df = st.data_editor(
                review_df,
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic",

                column_config={
                    "App": st.column_config.TextColumn(
                        "App Name",
                        required=True
                    ),

                    "Category": st.column_config.SelectboxColumn(
                        "Category",
                        options=[
                            "Social Media",
                            "Education",
                            "Entertainment",
                            "Coding",
                            "Other"
                        ],
                        required=True
                    ),

                    "Minutes Used": st.column_config.NumberColumn(
                        "Minutes Used",
                        min_value=0,
                        step=1,
                        required=True
                    )
                },

                key="screen_time_editor"
            )

            st.session_state.reviewed_screen_time = edited_review_df

            st.info(
                "Review the extracted values carefully. "
                "You can edit, add, or remove rows before importing."
            )

            if st.button(
                "✅ Verify & Import This Day",
                key="verify_import_screen_time"
            ):
                # Make a copy so we don't accidentally modify
                # the editable table directly
                import_df = edited_review_df.copy()

                # ---------- VALIDATE USER-EDITED DATA ----------

                import_df["App"] = import_df["App"].astype(str).str.strip()

                import_df["Category"] = import_df["Category"].fillna("Other")

                import_df["Minutes Used"] = pd.to_numeric(
                    import_df["Minutes Used"],
                    errors="coerce"
                )
                # Remove invalid rows
                import_df = import_df[
                    (import_df["App"] != "") &
                    (import_df["Minutes Used"].notna()) &
                    (import_df["Minutes Used"] >= 0)
                ].copy()

                if import_df.empty:

                    st.error(
                        "No valid screen-time data found. "
                        "Please check the table."
                    )

                else:
                     # ---------- PREVENT DUPLICATE DAY ----------

                    import_date_str = import_date.strftime("%Y-%m-%d")

                    existing_dates = (
                        st.session_state.edited_df["Date"]
                        .astype(str)
                        .unique()
                    )

                    if import_date_str in existing_dates:

                        st.warning(
                            f"⚠️ {import_date_str} already exists in "
                            "your Life-OS data. Please choose a new date."
                        )
                    else:

                        # ---------- CONVERT TO LIFE-OS FORMAT ----------

                        new_day_df = pd.DataFrame({
                            "Date": import_date_str,
                            "App_Name": import_df["App"],
                            "Category": import_df["Category"],
                            "Minutes_Used": import_df["Minutes Used"].astype(int)
                        })

                        # ---------- ADD NEW DAY ----------

                        st.session_state.edited_df = pd.concat(
                            [
                                st.session_state.edited_df,
                                new_day_df
                            ],
                             ignore_index=True
                        )

                        # Store imported date
                        st.session_state.imported_date = import_date_str

                        # Store verification state
                        st.session_state.screen_time_verified = True

                        st.success(
                            f"🎉 {import_date_str} has been imported "
                            "successfully into Life-OS!"
                        )
                        st.info(
                            "Your new day has been added to the current "
                            "Life-OS session."
                        )
                

                st.success(
                    "Data verified successfully! 🎉"
                )
        return screen_time_image

    if page == "🏠 Overview":
        welcome()
        show_usage()
        show_kpi()
        show_graph()
        show_ai()


    elif page == "🎭 Avatar Companion":
        st.header("🎭 Avatar Companion")
        show_usage()

    elif page == "📊 Performance":
        st.header("📊 Performance")
        show_kpi()

    elif page == "📈 Analytics":
        st.header("📈 Analytics")
        show_graph()
        edit()

    elif page == "🤖 AI Coach & Advance Features":
        st.header("🤖 AI Coach & Advance Features")
        show_ai()

    st.divider()

    st.caption(
        "🧠 Life-OS | AI Builder Internship Project | Powered by Gemini & Streamlit| Developer- Bhoomi Singhal"
    )
