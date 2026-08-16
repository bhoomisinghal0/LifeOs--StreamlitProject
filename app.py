import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
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




st.title("🧠 Your Personal Life-OS")

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



df = pd.read_csv("screentime.csv")

#initializing st.session_state
if "selected_day" not in st.session_state:
    st.session_state.selected_day= df["Date"].iloc[0]
if "goal" not in st.session_state:
    st.session_state.goal=240
if"ai_advice" not in st.session_state:
    st.session_state.ai_advice=None
if "avatar_day" not in st.session_state:
    st.session_state.avatar_day = None
if "avatar_url" not in st.session_state:
    st.session_state.avatar_url = None


st.sidebar.header("Controls 🕹️")


dates = sorted(df["Date"].unique())
selected_day = st.sidebar.selectbox("Choose date", dates, key="selected_day")

goal = st.sidebar.slider(
    "Daily Goal (in minutes)",
    20,  # min value
    600,  # max value
    240,  # default value
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
        "🤖 AI Coach",
    ],
    label_visibility="collapsed"
)


today_df = df[df["Date"] == selected_day].reset_index(
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


top_app = today_df.groupby("App_Name")["Minutes_Used"].sum().idxmax()

delta = goal - total_minutes


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


def show_graph():
    st.header("14 Days Screen-Time Trend")
    trend = df.groupby("Date")["Minutes_Used"].sum()
    st.subheader("📈 Screen Time Trend (14 Days)")

    st.line_chart(trend, height=350)


def show_ai():

    prompt = f"""
    You are Life-OS AI.

    Today's screen time:

    {summary_text}

    Goal: {goal} min
    Actual: {total_minutes} min

    Reply in under 100 words.

    Format exactly:

    Overall Score:
    Habit Analysis:
    2 Offline Alternatives:
    Motivation:

    If Coding is high, appreciate productive work.

    If Social Media is high, suggest outdoor or offline activities.

    If Entertainment is high, recommend healthier leisure.

    Never recommend reducing coding time.
    """

    if st.button("🤖 Get AI Advice"):
        try:
            with st.spinner("Analyzing your digital habits...🤖"):
                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )

                advice1 = response.choices[0].message.content

                st.session_state.ai_advice=advice1

                if total_minutes > goal:
                    st.warning(advice1)
                else:
                    st.info(advice1)

            

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
        specific_asked_query_prompt =f"""
        You are the AI Life Coach inside Life-OS.

        Your job is to analyze the user's digital habits and provide
        practical, realistic wellbeing advice.

        User's screen-time information:

        Date: {selected_day}
        Total screen time: {total_minutes} minutes
        Daily goal: {goal} minutes
        Most used app: {top_app}
        Category breakdown:
        {summary_text}
        user context:
        {user_context if user_context.strip() else "No additional context provided."}

        Give the user:

        1. Solution of user context based on their analysis of their digital habits.
        2. The main issue they should focus on.
        3. Three practical actions they can take.
        4. One simple goal for today.

        Keep the response concise, supportive, and practical.
        Do not give medical advice.
        """
        try:
            with st.spinner("Analyzing your digital habits... 🤖"):

                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": specific_asked_query_prompt 
                        }
                    ],
                    max_tokens=500
                )

                advice = response.choices[0].message.content
                st.success("Your personalized advice is ready!")

                st.info(advice)
        except Exception:
            st.warning(
                "🤖 AI Coach is temporarily unavailable. "
                "Your dashboard is still working normally."
            )

    if st.session_state.ai_advice:
        st.subheader("🧠 Your Latest AI Advice")
        st.info(st.session_state.ai_advice)


if page == "🏠 Overview":
    show_usage()
    show_kpi()
    show_graph()
    show_ai()


elif page == "🎭 Avatar Companion":
    show_usage()

elif page == "📊 Performance":
    show_kpi()

elif page == "📈 Analytics":
    show_graph()

elif page == "🤖 AI Coach":
    show_ai()

st.divider()

st.caption(
    "🧠 Life-OS | AI Builder Internship Project | Powered by Gemini & Streamlit| Developer- Bhoomi Singhal"
)
