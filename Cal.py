import streamlit as st
import json
from datetime import date

st.title("Calorie Tracker")

today = str(date.today())

# Load history once, and keep it in session_state so we don't
# re-read the file on every single rerun.
if "history" not in st.session_state:
    try:
        with open("food_history.json") as f:
            st.session_state.history = json.load(f)
    except FileNotFoundError:
        st.session_state.history = {}

if today not in st.session_state.history:
    st.session_state.history[today] = []

st.subheader("Log a food")
Food = st.text_input("Food Consumed?", key="food_input")
Cal = st.number_input("How many Calories?", min_value=0, step=1, key="cal_input")
Prot = st.number_input("Protein in g?", min_value=0, step=1, key="prot_input")
Fat = st.number_input("Fat in g?", min_value=0, step=1, key="fat_input")
Carb = st.number_input("Carbs in g?", min_value=0, step=1, key="carb_input")

if st.button("Add Food"):
    st.session_state.history[today].append({
        "Foods": Food, "Calories": Cal, "Protien": Prot, "Fat": Fat, "Carbs": Carb
    })
    with open("food_history.json", "w") as f:
        json.dump(st.session_state.history, f, indent=2)
    st.success(f"Added {Food}!")

def reset_inputs():
    st.session_state.food_input = ""
    st.session_state.cal_input = 0
    st.session_state.prot_input = 0
    st.session_state.fat_input = 0
    st.session_state.carb_input = 0

st.button("Reset Inputs", on_click=reset_inputs)

st.subheader(f"Today's Log ({today})")

if st.button("Undo Last Entry"):
    if st.session_state.history[today]:
        removed = st.session_state.history[today].pop()
        with open("food_history.json", "w") as f:
            json.dump(st.session_state.history, f, indent=2)
        st.warning(f"Removed: {removed['Foods']}")
    else:
        st.warning("Nothing to undo — today's log is empty.")

for entry in st.session_state.history[today]:
    st.write(f"{entry['Foods']} — {entry['Calories']} cal, {entry['Protien']}g protein, {entry['Fat']}g fat, {entry['Carbs']}g carbs")

total_Calories = sum(entry["Calories"] for entry in st.session_state.history[today])
total_Protien = sum(entry["Protien"] for entry in st.session_state.history[today])
total_Fat = sum(entry["Fat"] for entry in st.session_state.history[today])
total_Carbs = sum(entry["Carbs"] for entry in st.session_state.history[today])

st.subheader("Today's Totals")
st.write(f"Calories: {total_Calories}")
st.write(f"Protein: {total_Protien}")
st.write(f"Fat: {total_Fat}")
st.write(f"Carbs: {total_Carbs}")