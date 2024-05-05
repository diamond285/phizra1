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
group = st.text_input('Мектеп топшасы / Подгруппа школы')

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

    cols = st.columns(3)
    with cols[0]:
        student["grade"] = st.number_input("Сынып / Класс" + ' ' * x, step=1, min_value=1, max_value=12)
    with cols[1]:
        student["year"] = st.number_input("Туған жылы / Год рождения" + ' ' * x, step=1, min_value=2000, max_value=2024)
    with cols[2]:
        student["gender"] = st.selectbox("Жаныс / Пол" + ' ' * x, ['Ұл / Юноша', 'Қыз / Девушка'])
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
        st.code(students)
        import pandas as pd

        df = pd.DataFrame([{
            "Деңгей / Уровень": option,
            "Аудан / Район": district,
            "Мектеп / Школу": school,
            "Мектеп топшасы / Подгруппа школы": group,
            "Сайыстың атауы / Название соревнований": seb_name,
            "Cпорт түрі / Вид спорта": seb_type,
            "Басшының толық аты-жөні / ФИО руководителя": fio_trener,
            "Басшының нөмірі / Номер руководителя": nomer_trener,
            "Аты - жөні / Фамилия имя отчество участника": student['fullname'],
            "Сынып / Класс": student['grade'],
            "Туған жылы / Год рождения": student['year'],
            "Жаныс / Пол": student['gender']
        } for student in students])

        st.dataframe(df)

        from sqlalchemy import create_engine

        engine = create_engine('postgresql+psycopg2://avnadmin:AVNS_T4uu1xCbxFXHvmDVt63@didarlyzhaz2024-didarlyzhaz2024.e.aivencloud.com:19026/defaultdb')
        df.to_sql('all_register', if_exists='append', con=engine)
