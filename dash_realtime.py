import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title("Dashboard Transactions Bancaires - Temps Reel")

import random
types = ['CASH_OUT', 'TRANSFER', 'CASH_IN', 'PAYMENT', 'DEBIT']
df = pd.DataFrame([{
    'type': random.choice(types),
    'amount': round(random.uniform(10, 50000), 2),
    'isFraud': 1 if random.random() < 0.004 else 0
} for _ in range(10000)])

placeholder = st.empty()

for i in range(100, len(df), 1000):
    with placeholder.container():
        df_current = df.head(i)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", f"{len(df_current):,}")
        col2.metric("Fraudes detectees", f"{df_current['isFraud'].sum():,}")
        col3.metric("Montant total", f"${df_current['amount'].sum():,.2f}")

        by_type = df_current.groupby("type")["amount"].count().reset_index()
        fig1 = px.bar(by_type, x="type", y="amount", color="type", title=f"Transactions par type ({i:,})")
        st.plotly_chart(fig1, key=f"fig1_{i}")

        fraud = df_current[df_current["isFraud"]==1].groupby("type")["amount"].count().reset_index()
        if len(fraud) > 0:
            fig2 = px.pie(fraud, values="amount", names="type", title="Distribution des fraudes")
            st.plotly_chart(fig2, key=f"fig2_{i}")

    time.sleep(1)

st.success("Streaming termine !")
