import streamlit as st

# Initialize connection.
conn = st.experimental_connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from dimhorario;', ttl=600)

# Print results.
for coluna in df.itertuples():
    st.write(f"{coluna.horario} faz parte do turno da {coluna.turno}:")