import streamlit as st

# Initialize connection.
conn = st.experimental_connection('mysql', type='sql', username='root', password='1234', host='localhost', database='junobaseorigem', dialect = "mysql")


# Perform query.
df = conn.query('SELECT * from horario;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.Horario} faz parte do turno da {row.Turno}:")
