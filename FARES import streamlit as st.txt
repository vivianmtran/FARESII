import streamlit as st
import pandas as pd

st.set_page_config(page_title="Octaplex vs Plasma: Cost Impact (FARES-II)", layout="centered")
st.title("🔬 Octaplex vs Plasma Replacement – Cost Model (Based on FARES-II Study)")

st.markdown("""
This tool helps estimate **cost savings** when replacing **plasma with Octaplex** in cardiac surgery patients, based on the FARES-II study findings [(JAMA 2024)](https://jamanetwork.com/journals/jama/article-abstract/2832096).
""")

st.header("📥 Inputs")
col1, col2 = st.columns(2)

with col1:
    total_surgeries = st.number_input("Annual cardiac surgeries", min_value=0, value=1000)
    percent_plasma_use = st.slider("% requiring plasma replacement", 0, 100, 60)
    rbc_cost = st.number_input("Cost per RBC unit ($)", min_value=0, value=600)
    platelet_cost = st.number_input("Cost per platelet unit ($)", min_value=0, value=500)

with col2:
    bypassing_agent_cost = st.number_input("Cost per bypassing agent dose ($)", min_value=0, value=2500)
    hosp_day_cost = st.number_input("Cost per hospital day ($)", min_value=0, value=1500)
    days_reduced = st.slider("Hospital days reduced with Octaplex", 0.0, 5.0, 1.0, step=0.5)
    toggle_comparison = st.checkbox("Show side-by-side cost comparison", value=True)

# Calculations
eligible_patients = total_surgeries * (percent_plasma_use / 100)

savings_rbc = eligible_patients * rbc_cost  # 1 unit saved
savings_platelet = eligible_patients * platelet_cost * 1.5  # 1.5 units saved
savings_bypassing = eligible_patients * bypassing_agent_cost  # 1 unit saved
savings_hosp_days = eligible_patients * hosp_day_cost * days_reduced

total_savings = savings_rbc + savings_platelet + savings_bypassing + savings_hosp_days

# Output
st.header("💸 Projected Annual Savings")

st.metric("Eligible patients (Octaplex instead of Plasma)", f"{int(eligible_patients)}")
st.metric("Total Annual Savings ($)", f"${total_savings:,.0f}")

if toggle_comparison:
    st.subheader("💡 Savings Breakdown")
    breakdown_df = pd.DataFrame({
        'Category': ['RBC units saved', 'Platelets saved', 'Bypassing agents saved', 'Shorter hospital stay'],
        'Savings ($)': [savings_rbc, savings_platelet, savings_bypassing, savings_hosp_days]
    })

    st.bar_chart(breakdown_df.set_index('Category'))

    with st.expander("📁 Download Data"):
        st.download_button(
            label="Download savings breakdown as CSV",
            data=breakdown_df.to_csv(index=False).encode('utf-8'),
            file_name='fares_ii_cost_savings.csv',
            mime='text/csv'
        )

st.info("This model is for estimation purposes only and based on assumptions from the FARES-II study (JAMA, 2024). Customize inputs as needed.")
