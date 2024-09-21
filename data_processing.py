# data_processing.py

def calculate_bmi(weight, height):
    """Calculate the Body Mass Index (BMI)."""
    if height > 0:
        height_m = height / 100  # Convert cm to meters
        return weight / (height_m ** 2)
    return 0

def validate_inputs(name, age, blood_pressure, heart_rate, glucose):
    """Validate the essential inputs before submission."""
    if not name:
        return "Name cannot be empty."
    if age <= 0:
        return "Age must be greater than zero."
    if not blood_pressure or not validate_blood_pressure_format(blood_pressure):
        return "Invalid blood pressure format. Please enter in the format '120/80'."
    if heart_rate <= 0:
        return "Heart rate must be a positive value."
    if glucose <= 0:
        return "Fasting blood sugar must be a positive value."
    return None

def validate_blood_pressure_format(bp):
    """Validate the blood pressure format (e.g., 120/80)."""
    import re
    pattern_bp = r'^\d{2,3}/\d{2,3}$'
    return re.match(pattern_bp, bp)

def generate_summary(data):
    """Generate a summary of the comprehensive medical checkup report."""
    summary = f"""
    ### Summary of Input:
    - **Name:** {data['name']}
    - **Age:** {data['age']}
    - **Blood Pressure:** {data['blood_pressure']}
    - **Heart Rate:** {data['heart_rate']} bpm
    - **Fasting Blood Sugar:** {data['glucose']} mg/dL
    """
    
    # Add more fields to the summary based on the input
    summary += f"- **BMI:** {calculate_bmi(data['weight'], data['height']):.2f}\n"
    
    return summary
