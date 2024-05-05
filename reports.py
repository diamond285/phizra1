import streamlit as st

password = st.text_input('Введите пароль', type='password')

if password == 'qwerty123!!':
    button = st.button("Сформировать отчет")
    if button:
        with st.spinner('Формирование'):
            import pandas as pd
            import psycopg2

            conn = psycopg2.connect(dbname="defaultdb",
                                    user="avnadmin",
                                    password="AVNS_T4uu1xCbxFXHvmDVt63",
                                    host="didarlyzhaz2024-didarlyzhaz2024.e.aivencloud.com",
                                    port=19026)

            cur = conn.cursor()
            cur.execute('select * from all_register')
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
