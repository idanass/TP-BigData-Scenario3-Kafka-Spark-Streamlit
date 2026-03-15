import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title("🏦 Dashboard Transactions Bancaires - Temps Réel")

# Charger le dataset
import random
types = ['CASH_OUT', 'TRANSFER', 'CASH_IN', 'PAYMENT', 'DEBIT']
df = pd.DataFrame([{
    'type': random.choice(types),
    'amount': round(random.uniform(10, 50000), 2),
    'isFraud': 1 if random.random() < 0.004 else 0
} for _ in range(10000)])

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", f"{len(df):,}")
col2.metric("Fraudes détectées", f"{df['isFraud'].sum():,}")
col3.metric("Montant total", f"${df['amount'].sum():,.2f}")

# Graphique 1 - Transactions par type
st.subheader("Transactions par type")
by_type = df.groupby("type")["amount"].count().reset_index()
fig1 = px.bar(by_type, x="type", y="amount", color="type", title="Nombre de transactions par type")
st.plotly_chart(fig1)

# Graphique 2 - Fraudes
st.subheader("Fraudes par type")
fraud = df[df["isFraud"]==1].groupby("type")["amount"].count().reset_index()
fig2 = px.pie(fraud, values="amount", names="type", title="Distribution des fraudes")
st.plotly_chart(fig2)
