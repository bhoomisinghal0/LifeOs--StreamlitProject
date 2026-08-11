import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import urllib.parse  # help in building pollination url

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)
st.set_page_config(page_title="Life-OS", page_icon="🧠", layout="wide")


st.title("🧠 Your Personal Life-OS")

# Injecting Custom CSS to design
st.markdown(
    """
     <style>
    /* Background Canvas: Smooth Dark Indigo to Black Gradient */
    .stApp {
        background: linear-gradient(135deg, #05050a 0%, #0d0b18 50%, #150a21 100%);
        color: #f1ecf9;
        font-family: 'Inter', sans-serif;
    }

    /* Neon Typography & Captions */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px #7209b7, 0 0 20px #b5179e !important;
        letter-spacing: -0.5px;
    }

    [data-testid="stCaptionContainer"] {
        color: #e0c2f2 !important;
        font-weight: 600;
        text-shadow: 0 0 8px rgba(245, 247, 247, 0.6);
        font-size: 1rem !important;
    }

    
    /* Sidebar: Vibrant Purple to Deep Violet Neon Gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1235 0%, #11071c 60%, #05020a 100%);
        border-right: 2px solid #7b2ff7;
        box-shadow: 5px 0 25px rgba(123, 47, 247, 0.15);
    }

    section[data-testid="stSidebar"]{

     padding-top:-50px !important;

     padding-left:18px;

     padding-right:18px;

    }

    div[data-testid="stSelectbox"]{
margin-top:0px;
margin-bottom:0px;

}

section[data-testid="stSidebar"] h2{

font-size:22px;

font-weight:900;

}

div[data-baseweb="slider"] [role="slider"]{

background:#a855f7 !important;

box-shadow:0 0 15px #a855f7;

}

div[data-baseweb="slider"] div{

border-radius:20px;

}

div[data-testid="stSlider"]{

margin-top:0px;

margin-bottom:-30px;

}
    
    /* Match Sidebar text elements */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] label {
        color: #e2d5f3 !important;
    }

    /* Dashboard Headers with subtle Violet text shadow */
     h5, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(157, 78, 221, 0.3);
    }

    /*Main Header*/
    @import url('https://fonts.googleapis.com/css2?family=Parisienne&display=swap');
    h1{
        color: #ffffff !important;
        font-style:italic;
        font-family:'Parisienne', cursive;
        font-size:50px !important;
        text-align:center;
        text-decoration: underline;
        font-weight: 1000 !important;
        text-shadow: 0 0 10px rgba(44, 1, 82, 0.3);
        margin-top:0px !important;
        
    }
    
    @keyframes neonPulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    [data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow:
        0 0 20px rgba(123,47,247,0.6),
        0 0 40px rgba(181,23,158,0.35);
    }

    [data-testid="stMetric"] {
    background: linear-gradient(
        -45deg,
        #1a0f2e,
        #2d1457,
        #4c1d95,
        #6d28d9,
        #3b0764
    );

    background-size: 350% 350%;
    animation: neonPulse 8s ease infinite;

    border-radius: 16px;
    padding: 20px;

    border: 1px solid rgba(186, 104, 255, 0.35);

    box-shadow:
        0 0 12px rgba(123,47,247,0.35),
        0 0 25px rgba(114,9,183,0.25),
        inset 0 0 10px rgba(255,255,255,0.03);

    transition: all .3s ease;
     }
    
    [data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #ffffff !important;
    font-weight: 800 !important;
}



    /*Glowing Neon Interactive Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #7209b7, #b5179e) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 20px 34px !important;
        font-size: 60px  !important;
        font-weight: 1000 !important;
        box-shadow: 0 0 15px rgba(181, 23, 158, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        box-shadow: 0 0 25px #b5179e, 0 0 10px #4cc9f0 !important;
        transform: scale(1.03);
    }

    /* Neon Embedded Dataframe Matrix Table */
    .stDataFrame, div[data-testid="stTable"] {
        background: rgba(18, 9, 36, 0.85) !important;
        border: 2px solid #7209b7 !important;
        border-radius: 12px !important;
        padding: 10px !important;
        box-shadow: 0 0 20px rgba(114, 9, 183, 0.25) !important;
    }
    div[data-testid="stHorizontalBlock"] {
    display: flex;
    align-items: stretch;
    }
    div[data-testid="column"] {
    display: flex;
    flex-direction: column;
    }
    div[data-testid="column"] > div {
    flex: 1;
    display: flex;
    flex-direction: column;
    }
    
    /* Hide radio label */
[data-testid="stRadio"] label{
    font-size:0px;
}

/* Space between options */
[data-testid="stRadio"] > div{
    gap:12px;
}

/* Each navigation item */
[data-testid="stRadio"] div[role="radiogroup"] label{

    background:#1d1232;

    border:1px solid rgba(255,255,255,.08);

    border-radius:12px;

    padding:2px 8px;

    transition:.3s;

}

/* Hover */
[data-testid="stRadio"] div[role="radiogroup"] label:hover{

    background:#7b2ff7;

    transform:translateX(6px);

}



    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
<style>

.hero-subtitle{
    text-align:center;
    font-size:24px;
    color:#d8b4fe !important;
    font-weight:700;
    margin-top:-20px;
    margin-bottom:5px;
}

.hero-tagline{
    text-align:center;
    font-size:16px;
    color:#9ca3af !important;
    margin-bottom:40px !important;
}

</style>
""",
    unsafe_allow_html=True,
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


df = pd.read_csv("screentime.csv")


st.sidebar.header("Controls 🕹️")


dates = sorted(df["Date"].unique())
selected_day = st.sidebar.selectbox("Choose date", dates)

goal = st.sidebar.slider(
    "Daily Goal (in minutes)",
    20,  # min value
    600,  # max value
    240,  # default value
    step=10,
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
    "",
    [
        "🏠 Overview",
        "🎭 Avatar Companion",
        "📊 Performance",
        "📈 Analytics",
        "🤖 AI Coach",
    ],
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
    
    if total_minutes < goal:

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

    else:

        avatar_ai_prompt = f"""
        Create ONE highly detailed cinematic image-generation prompt.

        The character is a terrifying but visually interesting zombie sitting and
        mindlessly scrolling on a glowing smartphone.

        Show a zombie with pale decayed skin, messy hair, tired hollow eyes and a
        slouched posture, completely absorbed in the phone. The zombie should look
        addicted to endless scrolling. Surround it with a dark, slightly chaotic
        environment, scattered objects, eerie atmosphere and the cold blue glow of
        the smartphone illuminating its face.

        Use dramatic cinematic lighting, strong shadows, atmospheric fog, detailed
        textures, depth of field, dynamic composition and professional dark fantasy
        digital-art quality.

        The smartphone must be clearly visible and the zombie's attention must be
        focused on scrolling.

        No text, no captions, no logos, no UI, no statistics and no multiple scenes.

        Return ONLY the final image-generation prompt.
        Maximum 150 words.
        """
    avatar_response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[{"role": "user", "content": avatar_ai_prompt}],
        max_tokens=500
    )

    avatar_prompt = avatar_response.choices[0].message.content.strip()
    encoded_prompt = urllib.parse.quote(avatar_prompt)

    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    with coln2:

        colm1, colm2, colm3 = st.columns([1, 8, 1])

        with colm2:
            st.subheader("🎭 Life-OS Companion")
            try:
                st.image(image_url, width=220)
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
            except:
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

                advice = response.choices[0].message.content

                if total_minutes > goal:
                    st.warning(advice)
                else:
                    st.info(advice)

        except Exception as e:
            st.toast("Unable to generate AI advice.")


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
