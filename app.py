import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Impact of FARES II at Your Institution", layout="centered")
st.title("🏥 Impact of FARES II at Your Institution")

st.markdown("""
This tool models the clinical and economic impact of replacing Fresh Plasma (FP) with 4F-PCC (Octaplex) in cardiac surgery patients, based on findings from the **FARES-II** study.
""")

st.header("🔢 1. Clinical Input Parameters")

surgeries = st.number_input("Total number of cardiac surgeries per year:", min_value=0, value=1000)
plasma_pct = st.slider("% of patients requiring plasma replacement:", 0, 100, 15)
patients_receiving_plasma = surgeries * (plasma_pct / 100)

st.header("⚙️ 2. Customize Assumptions")
col1, col2 = st.columns(2)
with col1:
    cost_rbc_unit = st.number_input("💲 Cost per unit of RBC:", min_value=0, value=600)
    cost_platelet_unit = st.number_input("💲 Cost per unit of Platelets:", min_value=0, value=500)
    cost_bypass_agent = st.number_input("💲 Cost per unit of bypassing agent:", min_value=0, value=2500)
with col2:
    reduction_rbc = st.number_input("⬇️ RBC reduction per patient:", min_value=0.0, value=1.0)
    reduction_platelet = st.number_input("⬇️ Platelet reduction per patient:", min_value=0.0, value=1.5)
    reduction_bypass = st.number_input("⬇️ Bypassing agent reduction per patient:", min_value=0.0, value=1.0)

st.subheader("📈 Clinical Benefits of Octaplex (4F-PCC) vs FP")
clinical_benefits = {
    "Hemostatic Effectiveness": "+17.6%",
    "Serious Adverse Events": "-23%",
    "Acute Kidney Injury": "-45%",
    "Transfusion Needs": "-29%",
    "24-hr Blood Loss": "-25%"
}
st.dataframe(pd.DataFrame.from_dict(clinical_benefits, orient='index', columns=["Improvement"]))

st.header("📊 3. Outcome Projections")

per_patient_saving = (
    reduction_rbc * cost_rbc_unit
    + reduction_platelet * cost_platelet_unit
    + reduction_bypass * cost_bypass_agent
)
total_saving = per_patient_saving * patients_receiving_plasma

# Blood product totals saved
rbc_saved = reduction_rbc * patients_receiving_plasma
platelets_saved = reduction_platelet * patients_receiving_plasma
bypass_saved = reduction_bypass * patients_receiving_plasma

# Visualization data
cost_labels = ['RBC Savings', 'Platelet Savings', 'Bypassing Agent Savings']
cost_values = [reduction_rbc * cost_rbc_unit * patients_receiving_plasma,
               reduction_platelet * cost_platelet_unit * patients_receiving_plasma,
               reduction_bypass * cost_bypass_agent * patients_receiving_plasma]

st.markdown(f"**\n🧮 Patients receiving plasma per year:** `{int(patients_receiving_plasma)}`")

st.markdown("### 🧍 Per-Patient Blood Product Reduction")
st.markdown(f"- 🩸 RBC units saved: `{reduction_rbc}`")
st.markdown(f"- 🧪 Platelet units saved: `{reduction_platelet}`")
st.markdown(f"- 💉 Bypassing agent doses avoided: `{reduction_bypass}`")

st.markdown("### 🏥 Your Hospital Saves (Annually)")
st.markdown(f"- 🩸 RBC units saved: `{rbc_saved:,.1f}`")
st.markdown(f"- 🧪 Platelet units saved: `{platelets_saved:,.1f}`")
st.markdown(f"- 💉 Bypassing agent doses avoided: `{bypass_saved:,.1f}`")

# Cost savings visualization
fig, ax = plt.subplots()
ax.bar(cost_labels, cost_values, color=['#ff9999','#66b3ff','#99ff99'])
ax.set_ylabel('Cost Savings ($)')
ax.set_title('Annual Cost Savings by Blood Product Category')
st.pyplot(fig)

st.markdown("### 💰 Financial Impact")
st.markdown(f"**💰 Estimated cost savings per patient:** `${per_patient_saving:,.2f}`")
st.markdown(f"**💰 Total estimated annual savings:** `${total_saving:,.2f}`")

st.markdown("---")
st.caption("Based on FARES-II study (JAMA 2024) and user-defined cost assumptions.")
