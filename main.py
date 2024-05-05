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

sorev = ['Ашық ойындар / Подвижные игры',
         'Спорттық ойындар / Спортивные игры',
         'Ұлттық ойындар / Национальные игры']

seb_name = st.selectbox('Сайыстың атауы / Название соревнований', sorev)
seb_type = st.text_input('Cпорт түрі / Вид спорта')
fio_trener = st.text_input('Басшының толық аты-жөні / ФИО руководителя')
nomer_trener = st.text_input('Басшының нөмірі / Номер руководителя')
nums = st.number_input('Қатысушылар саны / Количество участников', step=1)

students = []
for x in range(nums):
    st.subheader("Қатысушы № {} / Участник № {}".format(x + 1, x + 1))
    student = dict()
    
    student['fullname'] = st.text_input("Аты - жөні / Фамилия имя отчество участника" + ' ' * x)

    cols = st.columns(3)
    with cols[0]:
        student["grade"] = st.number_input("Сынып / класс" + ' ' * x, step=1, min_value=1, max_value=12)
    with cols[1]:
        student["year"] = st.number_input("Туған жылы / Год рождения" + ' ' * x, step=1, min_value=2000, max_value=2024)
    with cols[2]:
        student["gender"] = st.selectbox("Пол" + ' ' * x, ['Ұл / Юноша', 'Қыз / Девушка'])

ok = True
if option is None or \
        school is None or \
        seb_name == '' or \
        seb_type == '' or \
        nums == 0:
    ok = False

submit = st.button("Отправить", disabled=not ok)
