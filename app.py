import streamlit as st
import pandas as pd
import os
from pycaret.regression import load_model, predict_model

# 🏷️ Title and Description
st.set_page_config(page_title="Cricket Score Predictor", layout="centered")
st.title("🏏 Cricket Score Predictor")
st.markdown("This is a PyCaret + Streamlit AutoML application to predict T20 match scores.")

# 📊 Model Comparison Table
if os.path.exists("logs/logs.csv"):
    st.subheader("📊 Model Performance Comparison")
    performance_df = pd.read_csv("logs/logs.csv")
    performance_df = performance_df.sort_values(by="R2", ascending=False)
    st.write(performance_df[["Model", "MAE", "MSE", "RMSE", "R2"]])
else:
    st.info("No model comparison log found. Re-run training notebook to generate logs.")

# 📥 Upload Test CSV OR Use Manual Input
st.subheader("📂 Predict Score")
option = st.radio("Choose input method:", ("Manual Input", "Upload CSV"))

# Load model
model = load_model("best_cricket_model")

if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with test data", type=["csv"])
    if uploaded_file:
        test_data = pd.read_csv(uploaded_file)
        st.write("📄 Uploaded Data Preview:")
        st.write(test_data)

        # Prediction
        predictions = predict_model(model, data=test_data)
        st.subheader("🎯 Predicted Scores")
        st.write(predictions[["prediction_label"]])  # or 'Label' based on pycaret version

else:
    st.markdown("🔧 **Enter Match Details Manually:**")
    overs_played = st.slider("Overs Played", 1, 20, 10)
    wickets_lost = st.slider("Wickets Lost", 0, 10, 3)
    run_rate = st.number_input("Current Run Rate", 0.0, 20.0, step=0.1)
    home_away = st.selectbox("Home or Away", ["Home", "Away"])
    opponent_strength = st.slider("Opponent Strength (1-10)", 1, 10, 5)
    pitch_condition = st.selectbox("Pitch Condition", ["Batting", "Bowling", "Balanced"])
    weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy"])

    input_df = pd.DataFrame({
        "match_id": [999],  # dummy ID
        "overs_played": [overs_played],
        "wickets_lost": [wickets_lost],
        "run_rate": [run_rate],
        "home/away": [home_away],
        "opponent_strength": [opponent_strength],
        "pitch_condition": [pitch_condition],
        "weather": [weather]
    })

    if st.button("Predict Score"):
        prediction = predict_model(model, data=input_df)
        predicted_score = prediction["prediction_label"][0]  # or 'Label'
        st.success(f"🏆 Predicted Final Score: **{int(predicted_score)}**")
