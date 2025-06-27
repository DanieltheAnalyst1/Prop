import streamlit as st
import pandas as pd

# Simulation function for Points Path
def simulate_points(traders, pass_rate_pct, withdraw_rate_pct, challenge_fee, net_p1, net_p2):
    pass_rate = pass_rate_pct / 100
    withdraw_rate = withdraw_rate_pct / 100
    rows = []
    for trader in traders:
        funded = trader * pass_rate
        expense = trader * challenge_fee
        net_m1 = funded * net_p1
        withdrawers_m2 = funded * withdraw_rate
        net_m2 = withdrawers_m2 * net_p2
        total_net = net_m1 + net_m2
        roi_m1 = (net_m1 / expense * 100) if expense > 0 else 0
        roi_combined = (total_net / expense * 100) if expense > 0 else 0

        rows.append({
            "Traders": trader,
            "Funded": round(funded, 1),
            "Expense (USD)": round(expense, 2),
            "Net Month 1 (USD)": round(net_m1, 2),
            "ROI Month 1 (%)": round(roi_m1, 1),
            "Withdrawers Month 2": round(withdrawers_m2, 1),
            "Net Month 2 (USD)": round(net_m2, 2),
            "Total Net (USD)": round(total_net, 2),
            "ROI Combined (%)": round(roi_combined, 1)
        })
    return pd.DataFrame(rows)

# Simulation for Direct-Purchase Path
def simulate_direct(traders, pass_rate_pct, net_direct):
    pass_rate = pass_rate_pct / 100
    rows = []
    for trader in traders:
        funded = trader * pass_rate
        net_m1_direct = funded * net_direct

        rows.append({
            "Traders": trader,
            "Funded": round(funded, 1),
            "Net Direct Month 1 (USD)": round(net_m1_direct, 2)
        })
    return pd.DataFrame(rows)

# Sidebar inputs
st.sidebar.header("Parameters")
traders_input = st.sidebar.text_input("Applicant Cohorts", "100,500,1000,5000,10000,20000,50000")
traders = [int(x.strip()) for x in traders_input.split(",")]

pass_rate_pct = st.sidebar.slider("Pass Rate (%)", 0, 100, 60, 5)
withdraw_rate_pct = st.sidebar.slider("Second Withdrawal Rate (%)", 0, 100, 40, 5)
challenge_fee = st.sidebar.number_input("Challenge Fee (USD)", 0.0, 100.0, 39.6, 0.1)
net_p1 = st.sidebar.number_input("Net Month 1 per Funded Trader (USD)", 0.0, 200.0, 98.6, 0.1)
net_p2 = st.sidebar.number_input("Net Month 2 per Funded Trader (USD)", 0.0, 200.0, 59.0, 0.1)
net_direct = st.sidebar.number_input("Net Direct per Funded Trader (USD)", 0.0, 50.0, 10.0, 0.1)

st.title("📊 Maven Partnership Simulator")

# Generate tables
df_points = simulate_points(traders, pass_rate_pct, withdraw_rate_pct, challenge_fee, net_p1, net_p2)
df_direct = simulate_direct(traders, pass_rate_pct, net_direct)

# Table 1: First-Month Results (Points Path)
st.subheader("Table 1: First-Month Results")
st.dataframe(df_points[["Traders", "Funded", "Expense (USD)", "Net Month 1 (USD)", "ROI Month 1 (%)"]])

# Mechanics & Thresholds
st.markdown("""
**Mechanics & Thresholds**  
- Challenge Fee (–10%): \$39.60 (fronted by our pool)  
- Points Needed: 500 ⇒ 1 pt = \$39.60/500 ≈ \$0.0792 of pool value  
- Pts per \$1 000 Volume: \$8.80 ÷ \$0.0792 ≈ 111 pts  
- Volume Required: 500 ÷ 111 ≈ 4 500 USD  
""")

# Core Unit Economics
st.markdown("**Core Unit Economics**")
core_table = pd.DataFrame({
    "Flow Volume": ["\$1 000"],
    "2% Spread": ["\$20.00"],
    "0.7% Fee (cap \$2)": ["\$2.00"],
    "Gross/1 000": ["\$22.00"],
    "Tech & Proc (20%)": ["\$4.40"],
    "Ops (40%)": ["\$8.80"],
    "Pool (40%)": ["\$8.80"]
})
st.table(core_table)
st.markdown("Whenever \$1 000 moves through your platform, \$8.80 credits the Points Pool.")

# Table 2: Two-Month Cohort Outcomes (Points Path Only)
st.subheader("Table 2: Two-Month Cohort Outcomes (Points Path Only)")
st.dataframe(df_points[["Traders", "Funded", "Expense (USD)", "Net Month 1 (USD)",
                        "Withdrawers Month 2", "Net Month 2 (USD)", "Total Net (USD)", "ROI Combined (%)"]])

# Table 3: Direct-Purchase Path (First-Month)

st.subheader("Table 3: Direct-Purchase Path (First-Month)")
# Direct-Purchase Core Mechanics table
st.markdown("Traders only withdraw 80% of profit (i.e. \$400 of a \$500 gain). No profit-share on this path.")
st.table(pd.DataFrame({
    "Item": ["2% Spread on \$400 withdrawn", "0.7% tx-fee (cap \$2)", "→ Net to Platform"],
    "Amount": ["\$8.00", "\$2.00", "\$10.00"]
}))

st.dataframe(df_direct[["Traders", "Funded", "Net Direct Month 1 (USD)"]])

# Table 4: Combined Two-Path First-Month Projection
combined = pd.DataFrame({
    "Traders": traders,
    "Points Path Net": df_points["Net Month 1 (USD)"],
    "Direct Path Net": df_direct["Net Direct Month 1 (USD)"],
    "Total Net Combined": df_points["Net Month 1 (USD)"] + df_direct["Net Direct Month 1 (USD)"]
})
st.subheader("Table 4: Combined Two-Path First-Month Projection")
st.dataframe(combined)

# Visualizations
st.subheader("Revenue Comparison")
st.bar_chart(combined.set_index("Traders")[["Points Path Net", "Direct Path Net"]])

