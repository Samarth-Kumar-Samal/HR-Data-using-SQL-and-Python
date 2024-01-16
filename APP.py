import streamlit as st
import pypyodbc as db
import programmer
import software
import education

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'SAM'
DATABASE_NAME = 'HR'

connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"
connection = db.connect(connection_string)
cursor = connection.cursor()
print("Connection Established")


if __name__ == '__main__' :

    st.title('HR DataBase')

    st.caption("This database helps in insertion of Programmer details, Software details and Education details")
    
    radio_option = st.radio('Choose from Table Options :',['None','Programmer','Software','Education','Display All Information'])

    if radio_option == 'Programmer' :
        st.info(f'You have selected {radio_option}')
        select_option = st.selectbox("Select an Opearation",['Choose an Operation','Create','Read','Update','Delete'])
        if select_option == 'Create' :
            st.info(f'You have selected {select_option} Operation')
            programmer.insert_record()
        elif select_option == 'Read' :
            st.info(f'You have selected {select_option} Operation')
            programmer.read_record()
        elif select_option == 'Update' :
            st.info(f'You have selected {select_option} Operation')
            programmer.update_record()
        elif select_option == 'Delete' :
            st.info(f'You have selected {select_option} Operation')
            programmer.delete_record()
        else :
            st.warning('Kindly select an operation from the given options')

    elif radio_option == 'Software' :
        st.info(f'You have selected {radio_option}')
        select_option = st.selectbox("Select an Opearation",['Choose an Operation','Create','Read','Update','Delete'])
        if select_option == 'Create' :
            st.info(f'You have selected {select_option} Operation')
            software.insert_record()
        elif select_option == 'Read' :
            st.info(f'You have selected {select_option} Operation')
            software.read_record()
        elif select_option == 'Update' :
            st.info(f'You have selected {select_option} Operation')
            software.update_record()
        elif select_option == 'Delete' :
            st.info(f'You have selected {select_option} Operation')
            software.delete_record()
        else :
            st.warning('Kindly select an operation from the given options')
    elif radio_option == 'Education' :
        st.info(f'You have selected {radio_option}')
        select_option = st.selectbox("Select an Opearation",['Choose an Operation','Create','Read','Update','Delete'])
        if select_option == 'Create' :
            st.info(f'You have selected {select_option} Operation')
            education.insert_record()
        elif select_option == 'Read' :
            st.info(f'You have selected {select_option} Operation')
            education.read_record()
        elif select_option == 'Update' :
            st.info(f'You have selected {select_option} Operation')
            education.update_record()
        elif select_option == 'Delete' :
            st.info(f'You have selected {select_option} Operation')
            education.delete_record()
        else :
            st.warning('Kindly select an operation from the given options')
    elif radio_option == 'Display All Information' :
        st.info(f'You have selected {radio_option}')
        st.subheader('READING RECORDS FROM ALL TABLES')
        cursor.execute('''
SELECT P.PROGRAMMER_ID,S.SOFTWARE_ID,P.FIRST_NAME,P.LAST_NAME,P.GENDER,P.PHONE,P.EMAIL,P.DATE_OF_BIRTH,P.DATE_OF_JOIN,P.PROF1,P.PROF2,P.SALARY,S.SOFTWARE_NAME,S.DEVELOPED_IN,S.COST_PRICE,S.SELL_PRICE,S.UNITS,E.INSTITUTE_NAME,E.COURSE_NAME,E.COURSE_FEE
FROM PROGRAMMER AS P
INNER JOIN SOFTWARE AS S
ON P.PROGRAMMER_ID = S.PROGRAMMER_ID
INNER JOIN EDUCATION AS E
ON E.SOFTWARE_ID = S.SOFTWARE_ID;
''')
        result = cursor.fetchall()
        columns = [str(column[0]).upper() for column in cursor.description]
        data_with_columns = [columns] + list(result)
        st.table(data_with_columns)

    else :
        st.warning('Kindly select any Table Operation from the given options')