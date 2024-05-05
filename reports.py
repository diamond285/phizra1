import streamlit as st

@st.cache_data
def load_schools():
    schools = []
    with open('schools', 'r') as f:
        for x in f.readlines():
            schools.append(x)
    return schools

password = st.text_input('Введите пароль', type='password')

if password == 'qwerty123!!':
    school = st.selectbox("Мектепті таңдаңыз / Выберите школу", ['-'] + load_schools())

    button = st.button("Сформировать отчет")
    
    if button and school == '-':
        with st.spinner('Формирование'):
            import pandas as pd
            import psycopg2

            conn = psycopg2.connect(dbname="defaultdb",
                                    user="avnadmin",
                                    password="AVNS_T4uu1xCbxFXHvmDVt63",
                                    host="didarlyzhaz2024-didarlyzhaz2024.e.aivencloud.com",
                                    port=19026)

            cur = conn.cursor()
            cur.execute('select * from test')
            tmp = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            df = pd.DataFrame(tmp, columns=colnames).drop(columns='index')
            import io
            buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Участники', index=False)
            writer.close()
            download2 = st.download_button(
                label="Скачать отчет",
                data=buffer,
                file_name='Дидарлы жаз 2024.xlsx',
                mime='application/vnd.ms-excel'
            )
    elif button and school != '-':
        with st.spinner('Формирование'):
            import pandas as pd
            import psycopg2

            conn = psycopg2.connect(dbname="defaultdb",
                                    user="avnadmin",
                                    password="AVNS_T4uu1xCbxFXHvmDVt63",
                                    host="didarlyzhaz2024-didarlyzhaz2024.e.aivencloud.com",
                                    port=19026)

            cur = conn.cursor()
            cur.execute(f'''select * from test where "Мектеп / Школа" = '{school}' ''')
            tmp = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            df = pd.DataFrame(tmp, columns=colnames).drop(columns='index')
            import io
            buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Участники', index=False)
            writer.close()
            download2 = st.download_button(
                label="Скачать отчет",
                data=buffer,
                file_name=f'Дидарлы жаз 2024 {school}.xlsx',
                mime='application/vnd.ms-excel'
            )
