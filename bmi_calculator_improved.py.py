import streamlit as st
import matplotlib.pyplot as plt

# Helper function for emojis (added for fun/UX)
def get_emoji(category):
    if category == "Underweight":
        return "🥦"
    elif category == "Normal weight":
        return "✅"
    elif category == "Overweight":
        return "⚠️"
    else:
        return "🚨"


# Modular function for BMI calculation (unchanged)
def calculate_bmi(weight, height):
    """
    Calculate BMI and return the value along with a health category.
    Formula: BMI = weight (kg) / (height (m))^2
    """
    if height <= 0 or weight <= 0:
        raise ValueError("Weight and height must be positive numbers.")
    
    bmi = weight / (height ** 2)
    
    # Determine category based on WHO standards
    if bmi < 18.5:
        category = "Underweight"
        color = "#FFD700"  # Yellow
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
        color = "#32CD32"  # Green
    elif 25 <= bmi < 30:
        category = "Overweight"
        color = "#FFA500"  # Orange
    else:
        category = "Obese"
        color = "#FF4500"  # Red
    
    return round(bmi, 2), category, color

# Custom CSS for better UI/UX
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 10px; margin: 10px 0; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #45a049; }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("🧮 BMI Calculator")
st.markdown("Calculate your Body Mass Index (BMI) easily. Enter your details below for instant results!")

# Input section with improved layout
st.header("📝 Enter Your Details")
col1, col2 = st.columns(2)  # Responsive columns for mobile

with col1:
    weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1, value=70.0, help="Your weight in kilograms (e.g., 70).")

with col2:
    height_unit = st.selectbox("Height Unit", ["Meters", "Centimeters"], help="Select your preferred unit.")
    if height_unit == "Meters":
        height = st.number_input("Height (m)", min_value=0.1, step=0.01, value=1.75, help="Your height in meters (e.g., 1.75).")
    else:
        height_cm = st.number_input("Height (cm)", min_value=1, step=1, value=175, help="Your height in centimeters (e.g., 175).")
        height = height_cm / 100  # Convert to meters

# Buttons for actions
col3, col4 = st.columns(2)
with col3:
    calculate = st.button("Calculate BMI", help="Click to compute your BMI.")
with col4:
    reset = st.button("Reset", help="Clear all inputs.")

if reset:
    st.rerun()  # Reset the app (fixed from st.experimental_rerun())

# Compute and display results
if calculate:
    try:
        bmi, category, color = calculate_bmi(weight, height)
        st.markdown(f'<div class="result-box" style="background-color:{color}20; border: 2px solid {color};">'
                    f'<p class="big-font">Your BMI: {bmi}</p>'
                    f'<p>Category: {category} {get_emoji(category)}</p>'
                    '</div>', unsafe_allow_html=True)
        st.info("💡 **Tip**: BMI is a general guide. Consult a doctor for health advice.")
        
        # Optional BMI chart for better UX
        st.subheader("📊 BMI Visualization")
        fig, ax = plt.subplots()
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
        ranges = [18.5, 25, 30, 40]  # Approximate upper bounds
        ax.barh(categories, ranges, color=['#FFD700', '#32CD32', '#FFA500', '#FF4500'])
        ax.axvline(x=bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi}')
        ax.legend()
        ax.set_xlabel('BMI Value')
        st.pyplot(fig)
        
    except ValueError as e:
        st.error(f"❌ Error: {e}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")

# Footer
st.write("---")
st.write("Built with Streamlit. Formula: BMI = weight (kg) / (height (m))^2")
st.write("For more on BMI, visit [WHO guidelines](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight).")