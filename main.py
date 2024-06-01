import streamlit as st


@st.cache_data
def load_schools():
    schools = []
    with open('schools', 'r') as f:
        for x in f.readlines():
            schools.append(x)
    return schools


st.header('Дидарлы жаз 2024')

levels = ['Қалалық деңгей / Городской уровень',
          'Республикалық деңгей / Республиканский уровень',
          'Халықаралық деңгей / Международный уровень']

option = st.selectbox("Деңгейді таңдаңыз / Выберите уровень", levels)

district = ''
if option == 'Қалалық деңгей / Городской уровень':
    districts = [
        'Алматы ауданы / Алматинский район',
        'Байқоныр ауданы / Байконурский район',
        'Есіл ауданы / Есильский район',
        'Нұра ауданы / Нуринский район (район «Нура»)',
        'Сарыарқа ауданы / Район Сарыарка'
    ]
    district = st.selectbox('Аудан / Район', districts)

school = st.selectbox("Мектепті таңдаңыз / Выберите школу", load_schools())
group = st.selectbox('Мектеп топшасы / Подгруппа школы', [x for x in range(1,11)])

sorev = ['Қозгалмалы ойындар / Подвижные игры',
         'Спорттық ойындар / Спортивные игры',
         'Ұлттық ойындар / Национальные игры']

seb_name = st.selectbox('Сайыстың атауы / Название соревнований', sorev)
seb_type = st.text_input('Cпорт түрі / Вид спорта')
fio_trener = st.text_input('Басшының толық аты-жөні / ФИО руководителя')
nomer_trener = st.text_input('Басшының нөмірі / Номер руководителя')
nums = st.number_input('Қатысушылар саны / Количество участников', step=1, min_value=1)

students = []
for x in range(nums):
    st.subheader("Қатысушы № {} / Участник № {}".format(x + 1, x + 1))
    student = dict()
    student['fullname'] = st.text_input("Аты - жөні / Фамилия имя отчество участника" + ' ' * x)

    cols = st.columns(2)
    with cols[0]:
        student['iin'] = st.text_input("ЖСН / ИИН" + ' ' * x)
    with cols[1]:
        student['phone'] = st.text_input("Телефон нөмірі / Номер телефона" + ' ' * x)

    cols = st.columns(3)
    with cols[0]:
        student["grade"] = st.number_input("Сынып / Класс" + ' ' * x, step=1, min_value=1, max_value=12)
    with cols[1]:
        student["year"] = st.number_input("Туған жылы / Год рождения" + ' ' * x, step=1, min_value=2000, max_value=2024)
    with cols[2]:
        student["gender"] = st.selectbox("Жыныс / Пол" + ' ' * x, ['Ұл / Юноша', 'Қыз / Девушка'])
    students.append(student)

ok = True
if option is None or \
        school is None or \
        seb_name == '' or \
        seb_type == '' or \
        nums == 0:
    ok = False

submit = st.button("Отправить", disabled=not ok)

if submit:
    with st.spinner('Сохранение'):
        import pandas as pd

        df = pd.DataFrame([{
            "Деңгей / Уровень": option,
            "Аудан / Район": district,
            "Мектеп / Школа": school,
            "Мектеп топшасы / Подгруппа школы": group,
            "Сайыстың атауы / Название соревнований": seb_name,
            "Cпорт түрі / Вид спорта": seb_type,
            "Басшының толық аты-жөні / ФИО руководителя": fio_trener,
            "Басшының нөмірі / Номер руководителя": nomer_trener,
            "Аты - жөні / Фамилия имя отчество участника": student['fullname'],
            "ЖСН / ИИН": student['iin'],
            "Телефон нөмірі / Номер телефона": student['phone'],
            "Сынып / Класс": student['grade'],
            "Туған жылы / Год рождения": student['year'],
            "Жыныс / Пол": student['gender']
        } for student in students])

        from sqlalchemy import create_engine

        engine = create_engine(
            'postgresql+psycopg2://avnadmin:AVNS_T4uu1xCbxFXHvmDVt63@didarlyzhaz2024-didarlyzhaz2024.e.aivencloud.com:19026/defaultdb')
        df.to_sql('test', if_exists='append', con=engine)

    with st.spinner('Формирование отчета'):
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
