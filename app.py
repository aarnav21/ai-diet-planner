import streamlit as st
from utils import calculate_bmi, calculate_bmr, calculate_tdee
from llm import generate_diet_plan

st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .metric-card {
        background-color: #f5f7fa;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🥗 NutriGen AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Your AI-powered personalized diet planner</div>',
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header("Enter Your Details")

age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=20)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

height = st.sidebar.number_input("Height (cm)", min_value=100, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=20, value=70)

activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Extra Active"
    ]
)

goal = st.sidebar.selectbox(
    "Goal",
    ["Lose Weight", "Gain Weight", "Maintain Weight"]
)

food_pref = st.sidebar.selectbox(
    "Food Preference",
    ["Vegetarian", "Non-Vegetarian", "Vegan"]
)

allergies = st.sidebar.text_input("Allergies")

generate = st.sidebar.button("Generate Diet Plan")

if generate:
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)

    if goal == "Lose Weight":
        calories = tdee - 500
    elif goal == "Gain Weight":
        calories = tdee + 500
    else:
        calories = tdee

    category = bmi_category(bmi)

    user_data = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "activity": activity,
        "goal": goal,
        "calories": round(calories),
        "food_pref": food_pref,
        "allergies": allergies
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>BMI</h3>
                <h2>{bmi}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Category</h3>
                <h2>{category}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Calories</h3>
                <h2>{round(calories)} kcal</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    try:
        with st.spinner("Generating your personalized AI diet plan..."):
            plan = generate_diet_plan(user_data)

        st.subheader("📋 Your Personalized Diet Plan")
        st.write(plan)

    except Exception:
        st.error("AI service temporarily unavailable. Please try again later.")