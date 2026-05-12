from groq import Groq
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

def generate_diet_plan(user_data):
    prompt = f"""
    Create a personalized 7-day Indian diet plan.

    User Details:
    Age: {user_data['age']}
    Gender: {user_data['gender']}
    Height: {user_data['height']} cm
    Weight: {user_data['weight']} kg
    BMI: {user_data['bmi']}
    Activity Level: {user_data['activity']}
    Goal: {user_data['goal']}
    Target Calories: {user_data['calories']}
    Food Preference: {user_data['food_pref']}
    Allergies: {user_data['allergies']}

    Requirements:
    - Indian meal plan
    - Breakfast, lunch, snacks, dinner
    - Mention calories
    - High protein
    - Student-friendly meals
    - Clean formatted output
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content