import pandas as pd
import numpy as np


def compute_metrics(df, wa, ws, wq):
    """The core logic being tested."""
    df = df.copy()
    # Risk Formula: (100 - Score) * Weight
    df["Risk Score"] = (
        (100 - df["Attendance (%)"]) * wa +
        (100 - df["Avg Score (%)"]) * ws +
        (100 - df["Quiz Score (%)"]) * wq
    )
    # Anomaly Logic: Drop of more than 15% from history
    df["Delta (Quiz - Avg)"] = df["Quiz Score (%)"] - df["Avg Score (%)"]
    df["Anomaly"] = df["Delta (Quiz - Avg)"] < -15

    mean_avg = df["Avg Score (%)"].mean()
    mean_quiz = df["Quiz Score (%)"].mean()

    def categorize(row):
        high_avg = row["Avg Score (%)"] >= mean_avg
        high_quiz = row["Quiz Score (%)"] >= mean_quiz
        if high_avg and high_quiz: return "High Flyers"
        elif high_avg and not high_quiz: return "Sudden Dip"
        elif not high_avg and high_quiz: return "The Climbers"
        else: return "Critical Support"

    df["Category"] = df.apply(categorize, axis=1)
    return df

# ──────────────────────────────────────────────────────────
# TEST SUITE
# ──────────────────────────────────────────────────────────

def run_tests():
    print("🚀 Initializing Test Suite for Student Analytics Engine...\n")

    # --- TEST 1: WEIGHT SENSITIVITY ---
    # High Grades (100) but Low Attendance (0). 
    # If Attendance weight is high, Risk should be high.
    test_data = pd.DataFrame({
        "Name": ["Test Student"],
        "Attendance (%)": [0],
        "Avg Score (%)": [100],
        "Quiz Score (%)": [100]
    })

    # Case A: Attendance weighted at 80%
    res_a = compute_metrics(test_data, wa=0.8, ws=0.1, wq=0.1)
    risk_high = res_a.iloc[0]["Risk Score"] # Should be 80

    # Case B: Attendance weighted at 10%
    res_b = compute_metrics(test_data, wa=0.1, ws=0.45, wq=0.45)
    risk_low = res_b.iloc[0]["Risk Score"] # Should be 10

    assert risk_high > risk_low
    print(f"✅ TEST 1 PASSED: Weight Customization correctly scales Risk ({risk_high} vs {risk_low}).")


    # --- TEST 2: ANOMALY DETECTION ---
    # Student drops from 90% history to 60% quiz.
    anomaly_data = pd.DataFrame({
        "Name": ["Nisha Reddy"],
        "Attendance (%)": [100],
        "Avg Score (%)": [90],
        "Quiz Score (%)": [60]
    })
    res_anomaly = compute_metrics(anomaly_data, 0.33, 0.33, 0.34)
    
    assert res_anomaly.iloc[0]["Anomaly"] == True
    print("✅ TEST 2 PASSED: Academic Anomaly detected for >15% performance drop.")


    # --- TEST 3: QUADRANT MAPPING ---
    # Create a 'High Flyer' and a 'Critical Support' to check relative mean logic.
    quad_data = pd.DataFrame({
        "Name": ["Aisha", "Rahul"],
        "Attendance (%)": [100, 100],
        "Avg Score (%)": [90, 40],
        "Quiz Score (%)": [90, 40]
    })
    res_quad = compute_metrics(quad_data, 0.33, 0.33, 0.34)
    
    assert res_quad.loc[res_quad['Name'] == "Aisha", "Category"].values[0] == "High Flyers"
    assert res_quad.loc[res_quad['Name'] == "Rahul", "Category"].values[0] == "Critical Support"
    print("✅ TEST 3 PASSED: Quadrant Logic correctly mapped students relative to class mean.")

    print("\n✨ ALL TESTS PASSED SUCCESSFULLY! Logic is verified and ready for deployment.")

if __name__ == "__main__":
    run_tests()