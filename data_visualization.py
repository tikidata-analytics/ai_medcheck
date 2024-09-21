import plotly.graph_objects as go

def create_gauge_chart(value, title, min_val, max_val, thresholds, units):
    if len(thresholds) < 2:
        raise ValueError("Thresholds must have at least two values: [low, high]")
    
    steps = []
    
    # Loop through thresholds to create multiple color bands
    for i in range(len(thresholds) + 1):
        if i == 0:
            steps.append({'range': [min_val, thresholds[i]], 'color': "lightblue"})  # Underweight
        elif i == len(thresholds):
            steps.append({'range': [thresholds[i-1], max_val], 'color': "red"})  # Obesity
        else:
            steps.append({'range': [thresholds[i-1], thresholds[i]], 'color': "green" if i == 1 else "yellow"})  # Normal weight and overweight
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"{title} ({units})"},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'steps': steps,
        }
    ))
    
    return fig
