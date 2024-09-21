import streamlit as st
import pandas as pd
import json
from data_processing import calculate_bmi, validate_inputs
from data_visualization import create_gauge_chart

# Sidebar content
with st.sidebar:
    st.title("Medical Checkup Report Dashboard")
    st.write("This app helps you understand your Medical Checkup Report so you can take action immediately without having a doctor examine the results.")
    st.write("The following configurations are ideal numbers for each metric. You can adjust them as you like, and it will affect all the charts to help you understand your current health position.")
    st.write("The app won't remember any personal information. Use it on your own.")

    # Editable ideal ranges for each metric in the sidebar with two columns layout
    st.subheader("Set Ideal Ranges")

    col1, col2 = st.columns(2)
    with col1:
        # Existing metrics
        systolic_low = st.number_input("Systolic BP (Low)", min_value=80, max_value=130, value=120)
        diastolic_low = st.number_input("Diastolic BP (Low)", min_value=50, max_value=90, value=80)
        heart_rate_low = st.number_input("Heart Rate (Low)", min_value=50, max_value=100, value=60)
        glucose_low = st.number_input("Glucose (Low)", min_value=60, max_value=140, value=100)
        cholesterol_total_low = st.number_input("Cholesterol (Low)", min_value=100, max_value=240, value=200)
        ldl_low = st.number_input("LDL Cholesterol (Low)", min_value=50, max_value=160, value=100)
        hdl_low = st.number_input("HDL Cholesterol (Low)", min_value=20, max_value=60, value=40)
        triglycerides_low = st.number_input("Triglycerides (Low)", min_value=50, max_value=150, value=150)
        
        # New kidney, liver, thyroid, electrolyte metrics
        creatinine_low = st.number_input("Creatinine (Low)", min_value=0.5, max_value=1.5, value=0.7)
        gfr_low = st.number_input("GFR (Low)", min_value=60, max_value=90, value=60)
        ast_low = st.number_input("AST (Low)", min_value=10, max_value=50, value=10)
        alt_low = st.number_input("ALT (Low)", min_value=10, max_value=50, value=10)
        tsh_low = st.number_input("TSH (Low)", min_value=0.4, max_value=4.0, value=0.4)
        sodium_low = st.number_input("Sodium (Low)", min_value=135, max_value=145, value=135)
        potassium_low = st.number_input("Potassium (Low)", min_value=3.5, max_value=5.0, value=3.5)
        hba1c_low = st.number_input("HbA1c (Low)", min_value=4.0, max_value=6.5, value=5.7)  # HbA1c Low

    with col2:
        # Existing metrics
        systolic_high = st.number_input("Systolic BP (High)", min_value=80, max_value=200, value=140)
        diastolic_high = st.number_input("Diastolic BP (High)", min_value=50, max_value=120, value=90)
        heart_rate_high = st.number_input("Heart Rate (High)", min_value=50, max_value=200, value=100)
        glucose_high = st.number_input("Glucose (High)", min_value=60, max_value=200, value=140)
        cholesterol_total_high = st.number_input("Cholesterol (High)", min_value=100, max_value=300, value=240)
        ldl_high = st.number_input("LDL Cholesterol (High)", min_value=50, max_value=200, value=160)
        hdl_high = st.number_input("HDL Cholesterol (High)", min_value=20, max_value=100, value=60)
        triglycerides_high = st.number_input("Triglycerides (High)", min_value=50, max_value=300, value=200)
        
        # New kidney, liver, thyroid, electrolyte metrics
        creatinine_high = st.number_input("Creatinine (High)", min_value=0.5, max_value=1.5, value=1.2)
        gfr_high = st.number_input("GFR (High)", min_value=60, max_value=120, value=90)
        ast_high = st.number_input("AST (High)", min_value=10, max_value=50, value=40)
        alt_high = st.number_input("ALT (High)", min_value=10, max_value=50, value=40)
        tsh_high = st.number_input("TSH (High)", min_value=0.4, max_value=10.0, value=4.0)
        sodium_high = st.number_input("Sodium (High)", min_value=135, max_value=155, value=145)
        potassium_high = st.number_input("Potassium (High)", min_value=3.5, max_value=6.0, value=5.0)
        hba1c_high = st.number_input("HbA1c (High)", min_value=4.0, max_value=15.0, value=6.5)  # HbA1c High

    st.markdown("Developed by [Tikidata Analytics](https://linktr.ee/tikidata_analytics)")
    st.markdown("Visit [Asuransimurni.com](https://asuransimurni.com) to find a Health Insurance with reasonable premiums.")

# Dropdown menu to select the type of checkup
checkup_type = st.selectbox("Select the type of checkup", ["Basic Medical Checkup", "Comprehensive Medical Checkup"])

# Define which sections should be shown for each type of checkup
if checkup_type == "Basic Medical Checkup":
    active_tabs = ["Personal Information", "Vital Signs", "Diabetes Check"]
else:
    active_tabs = ["Personal Information", "Vital Signs", "Lipid Panel", "Kidney Function", "Liver Function", "Thyroid Function", "Electrolytes", "Diabetes Check"]

# Create tabs based on the selected checkup type
tabs = st.tabs([tab for tab in active_tabs])

# 1. Personal Information
with tabs[0]:
    st.header("Personal Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.radio("Gender", ("Male", "Female"))

    # Add height and weight here
    weight = st.number_input("Weight (kg)", min_value=0.0, format="%.1f")
    height = st.number_input("Height (cm)", min_value=0.0, format="%.1f")

    # Automatically display BMI gauge when both weight and height are provided
    if weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height)
        st.success(f"Your BMI is: {bmi:.2f}")

        with st.expander("BMI Checkup"):
            st.subheader("BMI")
            st.plotly_chart(create_gauge_chart(bmi, "BMI", 10, 40, [18.5, 24.9, 29.9], "kg/m²"))
            
            # BMI interpretation with encouraging language
            if bmi < 18.5:
                st.error("You are underweight. 🍽️ A healthy diet with more calories from nutritious sources like nuts, whole grains, and lean proteins can help. You can achieve your goals! 💪")
            elif 18.5 <= bmi < 24.9:
                st.success("Your BMI is in the normal range. 🏆 Keep up the great work! Stay on track with a balanced diet and regular exercise.")
            elif 25 <= bmi < 29.9:
                st.error("You are overweight. 🍏 Focus on portion control and adding more physical activities to your routine. You’ve got this! 💥")
            else:
                st.error("You are in the obese range. 🏋️‍♂️ Start with small steps by adjusting your diet and increasing physical activity. You can make a big difference! 🌟")

# 2. Vital Signs (available for both checkup types)
with tabs[1]:
    st.header("Vital Signs")
    blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=200, step=1)

    # Display Blood Pressure and Heart Rate gauges when values are provided
    if blood_pressure and "/" in blood_pressure:
        systolic, diastolic = map(int, blood_pressure.split('/'))

        if systolic > 0:
            st.plotly_chart(create_gauge_chart(systolic, "Systolic BP", 80, 200, [systolic_low, systolic_high], "mmHg"))
            if systolic_low <= systolic <= systolic_high:
                st.success("Your systolic blood pressure is in the normal range. 🏆 Keep up the healthy lifestyle!")
            else:
                st.error("Your systolic blood pressure is outside the normal range. 🧘‍♂️ Try managing stress, limiting salt intake, and staying active to improve.")

        if diastolic > 0:
            st.plotly_chart(create_gauge_chart(diastolic, "Diastolic BP", 50, 120, [diastolic_low, diastolic_high], "mmHg"))
            if diastolic_low <= diastolic <= diastolic_high:
                st.success("Your diastolic blood pressure is in the normal range. 💓 Great job maintaining your health!")
            else:
                st.error("Your diastolic blood pressure is outside the normal range. 🏃‍♂️ Regular exercise and a balanced diet can help lower your blood pressure.")

    if heart_rate > 0:
        st.plotly_chart(create_gauge_chart(heart_rate, "Heart Rate", 50, 200, [heart_rate_low, heart_rate_high], "bpm"))
        if heart_rate_low <= heart_rate <= heart_rate_high:
            st.success("Your heart rate is in a healthy range. 💓 Keep up the good work!")
        else:
            st.error("Your heart rate is outside the healthy range. 🏃‍♂️ Consider regular aerobic exercises and stress management to improve.")

# 3. Lipid Panel (only available for comprehensive checkup)
if "Lipid Panel" in active_tabs:
    with tabs[2]:
        st.header("Lipid Panel")
        total_cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=0)
        ldl = st.number_input("LDL Cholesterol (mg/dL)", min_value=0)
        hdl = st.number_input("HDL Cholesterol (mg/dL)", min_value=0)
        triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=0)

        if total_cholesterol > 0:
            st.plotly_chart(create_gauge_chart(total_cholesterol, "Total Cholesterol", 100, 300, [cholesterol_total_low, cholesterol_total_high], "mg/dL"))
            if total_cholesterol <= cholesterol_total_high:
                st.success("Your total cholesterol is within a healthy range. 🌟 Keep up the good work!")
            else:
                st.error("Your total cholesterol is high. 🍽️ Incorporate more whole grains, vegetables, and healthy fats into your diet.")

        if ldl > 0:
            st.plotly_chart(create_gauge_chart(ldl, "LDL Cholesterol", 50, 200, [ldl_low, ldl_high], "mg/dL"))
            if ldl <= ldl_high:
                st.success("Your LDL cholesterol is at a healthy level. 🏅 Keep it up!")
            else:
                st.error("Your LDL cholesterol is too high. 🥑 Focus on reducing saturated fats and increasing fiber.")

        if hdl > 0:
            st.plotly_chart(create_gauge_chart(hdl, "HDL Cholesterol", 20, 100, [hdl_low, hdl_high], "mg/dL"))
            if hdl >= hdl_low:
                st.success("Your HDL cholesterol is at a good level. 👍 Keep maintaining those healthy habits!")
            else:
                st.error("Your HDL cholesterol is low. 🥗 Add more healthy fats like olive oil and avocado to your diet.")

        if triglycerides > 0:
            st.plotly_chart(create_gauge_chart(triglycerides, "Triglycerides", 50, 300, [triglycerides_low, triglycerides_high], "mg/dL"))
            if triglycerides <= triglycerides_high:
                st.success("Your triglycerides are within a healthy range. 🎉 Great job!")
            else:
                st.error("Your triglycerides are high. 🍏 Focus on reducing sugar intake and increasing physical activity.")

# 4. Kidney Function (only available for comprehensive checkup)
if "Kidney Function" in active_tabs:
    with tabs[3]:
        st.header("Kidney Function")
        creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, max_value=10.0, step=0.1)
        gfr = st.number_input("Glomerular Filtration Rate (GFR)", min_value=0, max_value=150, step=1)

        if creatinine > 0:
            st.plotly_chart(create_gauge_chart(creatinine, "Creatinine", 0.0, 10.0, [creatinine_low, creatinine_high], "mg/dL"))
            if creatinine <= creatinine_high:
                st.success("Your creatinine levels are healthy! 💧 Keep up the hydration and balanced diet!")
            else:
                st.error("Your creatinine levels are high. 🥛 Stay hydrated and consider seeing a healthcare provider.")

        if gfr > 0:
            st.plotly_chart(create_gauge_chart(gfr, "GFR", 0, 150, [gfr_low, gfr_high], "mL/min"))
            if gfr >= gfr_low:
                st.success("Your GFR is within the healthy range. 🌿 Keep supporting your kidneys with a healthy lifestyle.")
            else:
                st.error("Your GFR is low. 🍵 Stay hydrated and consider consulting a doctor.")

# 5. Liver Function (only available for comprehensive checkup)
if "Liver Function" in active_tabs:
    with tabs[4]:
        st.header("Liver Function")
        ast = st.number_input("AST (U/L)", min_value=0, max_value=200, step=1)
        alt = st.number_input("ALT (U/L)", min_value=0, max_value=200, step=1)

        if ast > 0:
            st.plotly_chart(create_gauge_chart(ast, "AST", 0, 200, [ast_low, ast_high], "U/L"))
            if ast <= ast_high:
                st.success("Your AST levels are in the normal range. 🌟 Keep up the healthy living!")
            else:
                st.error("Your AST levels are high. 🍵 Reduce alcohol intake and consider liver-friendly foods like leafy greens.")

        if alt > 0:
            st.plotly_chart(create_gauge_chart(alt, "ALT", 0, 200, [alt_low, alt_high], "U/L"))
            if alt <= alt_high:
                st.success("Your ALT levels are healthy. 🍏 Great job supporting your liver!")
            else:
                st.error("Your ALT levels are high. 🍃 Focus on liver health by eating more fiber-rich foods and reducing fatty meals.")

# 6. Thyroid Function (only available for comprehensive checkup)
if "Thyroid Function" in active_tabs:
    with tabs[5]:
        st.header("Thyroid Function")
        tsh = st.number_input("TSH (µU/mL)", min_value=0.0, max_value=10.0, step=0.1)

        if tsh > 0:
            st.plotly_chart(create_gauge_chart(tsh, "TSH", 0.0, 10.0, [tsh_low, tsh_high], "µU/mL"))
            if tsh <= tsh_high:
                st.success("Your thyroid function is normal. 🦋 Keep up the great work!")
            else:
                st.error("Your TSH levels are off. 💡 Consult with your healthcare provider to manage your thyroid health.")

# 7. Electrolytes (only available for comprehensive checkup)
if "Electrolytes" in active_tabs:
    with tabs[6]:
        st.header("Electrolytes")
        
        # Set default value to a valid numeric type (e.g., 0) and handle it in the logic below
        sodium = st.number_input("Sodium (mEq/L)", min_value=0.0, max_value=200.0, step=1.0, value=0.0)
        potassium = st.number_input("Potassium (mEq/L)", min_value=0.0, max_value=10.0, step=0.1, value=0.0)

        # Only show the gauge if the input is greater than 0 (i.e., a valid user input)
        if sodium > 0:
            st.plotly_chart(create_gauge_chart(sodium, "Sodium", 100, 200, [sodium_low, sodium_high], "mEq/L"))
            if sodium <= sodium_high:
                st.success("Your sodium levels are within the healthy range. 💧 Keep hydrated and stay balanced!")
            else:
                st.error("Your sodium levels are high. 🧂 Consider reducing salt intake and staying hydrated.")

        if potassium > 0:
            st.plotly_chart(create_gauge_chart(potassium, "Potassium", 2.0, 10.0, [potassium_low, potassium_high], "mEq/L"))
            if potassium >= potassium_low and potassium <= potassium_high:
                st.success("Your potassium levels are normal. 🍌 Great job maintaining a healthy diet!")
            else:
                st.error("Your potassium levels are outside the normal range. 🥑 Adjust your diet to include more potassium-rich foods or consult a healthcare provider.")


# 8. Diabetes Check (available for both checkup types)
with tabs[-1]:
    st.header("Diabetes Check")
    glucose = st.number_input("Fasting Blood Sugar (mg/dL)", min_value=0.0)
    hba1c = st.number_input("Hemoglobin A1c (HbA1c) (%)", min_value=0.0, max_value=15.0, step=0.1)

    if glucose > 0:
        st.plotly_chart(create_gauge_chart(glucose, "Glucose", 60, 200, [glucose_low, glucose_high], "mg/dL"))
        if glucose <= glucose_high:
            st.success("Your fasting blood sugar is within a healthy range. 🎉 Keep up the balanced diet!")
        else:
            st.error("Your glucose levels are high. 🍬 Consider cutting down on sugar and focusing on whole foods to improve your levels.")

    if hba1c > 0:
        st.plotly_chart(create_gauge_chart(hba1c, "HbA1c", 4.0, 15.0, [hba1c_low, hba1c_high], "%"))
        if hba1c <= hba1c_high:
            st.success("Your HbA1c is under control. 🏅 Keep managing your blood sugar with healthy lifestyle choices!")
        else:
            st.error("Your HbA1c is high. 🍓 Focus on improving your diet and staying physically active to reduce your A1c levels.")
