import streamlit as st
import pypyodbc as db

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'SAM'
DATABASE_NAME = 'HR'


connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"
connection = db.connect(connection_string)
cursor = connection.cursor()

# ******************************
# Insert Operation Function
# ******************************

def insert_record():
    st.subheader("CREATE A PROGRAMMER RECORD")
    first_name = st.text_input('ENTER THE FIRST NAME OF THE PROGRAMMER : ')
    last_name = st.text_input('ENTER THE LAST NAME OF THE PROGRAMMER : ')
    gender = st.radio('ENTER THE GENDER OF THE PROGRAMMER : ', ['Male', 'Female'])
    phone = st.text_input('ENTER THE PHONE NUMBER OF THE PROGRAMMER :')
    email = st.text_input('ENTER THE EMAIL ID OF THE PROGRAMMER :')
    dob = st.date_input('ENTER THE DATE OF BIRTH OF THE PROGRAMMER :', value='today')
    doj = st.date_input('ENTER THE DATE OF JOIN OF THE PROGRAMMER :', value='today')
    prof1 = st.text_input('ENTER THE FIRST PROFICIENCY PROGRAMMING LANGUAGE OF THE PROGRAMMER :')
    prof2 = st.text_input('ENTER THE SECOND PROFICIENCY PROGRAMMING LANGUAGE OF THE PROGRAMMER :')
    salary = st.number_input('ENTER THE SALARY OF THE PROGRAMMER :', value=0)

    if st.button('Create'):
        if exist_record(first_name, last_name, gender, phone, email, salary):
            st.error('Record Already Exists')
        else:
            cursor.execute(
                'INSERT INTO PROGRAMMER(FIRST_NAME,LAST_NAME,GENDER,PHONE,EMAIL,DATE_OF_BIRTH,DATE_OF_JOIN,PROF1,PROF2,SALARY) VALUES(?,?,?,?,?,?,?,?,?,?)',
                (first_name, last_name, gender, phone, email, dob, doj, prof1, prof2, salary))
            connection.commit()
            st.success('Record Created Successfully')


# ***********************************
# Checking Existing Record Function
# ***********************************

def exist_record(first_name, last_name, gender, phone, email, salary):
    cursor.execute(
        'SELECT * FROM PROGRAMMER WHERE FIRST_NAME = ? AND LAST_NAME = ? AND GENDER = ? AND PHONE = ? AND EMAIL = ? AND SALARY = ?',
        (first_name, last_name, gender, phone, email, salary))
    existing_record = cursor.fetchone()
    return existing_record is not None


# ******************************
# Reading Operation Function
# ******************************

def read_record():
    st.subheader('READING RECORDS FROM PROGRAMMER TABLE')
    cursor.execute('SELECT * FROM PROGRAMMER')
    result = cursor.fetchall()
    columns = [str(column[0]).upper() for column in cursor.description]
    data_with_columns = [columns] + list(result)
    st.table(data_with_columns)

# ******************************
# Update Operation Function
# ******************************

def update_record():
    st.subheader('UPDATE RECORD IN PROGRAMMER TABLE')
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID :',value=0)
    cursor.execute("SELECT * FROM PROGRAMMER WHERE PROGRAMMER_ID = ?", (programmer_id,))
    existing_record = cursor.fetchone()

    if not existing_record:
        st.error(f'Record with ID {programmer_id} not found. Unable to update.')
        return
    first_name = st.text_input('ENTER THE FIRST NAME OF THE PROGRAMMER : ')
    last_name = st.text_input('ENTER THE LAST NAME OF THE PROGRAMMER : ')
    gender = st.radio('ENTER THE GENDER OF THE PROGRAMMER : ', ['Male', 'Female'])
    phone = st.text_input('ENTER THE PHONE NUMBER OF THE PROGRAMMER :')
    email = st.text_input('ENTER THE EMAIL ID OF THE PROGRAMMER :')
    dob = st.date_input('ENTER THE DATE OF BIRTH OF THE PROGRAMMER :', value='today')
    doj = st.date_input('ENTER THE DATE OF JOIN OF THE PROGRAMMER :', value='today')
    prof1 = st.text_input('ENTER THE FIRST PROFICIENCY PROGRAMMING LANGUAGE OF THE PROGRAMMER :')
    prof2 = st.text_input('ENTER THE SECOND PROFICIENCY PROGRAMMING LANGUAGE OF THE PROGRAMMER :')
    salary = st.number_input('ENTER THE SALARY OF THE PROGRAMMER :', min_value=0)
    
    if st.button('Update'):
        cursor.execute(
            'UPDATE PROGRAMMER SET FIRST_NAME = ?,LAST_NAME = ?,GENDER = ?,PHONE = ?,EMAIL = ?,DATE_OF_BIRTH = ?, DATE_OF_JOIN = ?, PROF1 = ?, PROF2 = ?, SALARY = ? WHERE PROGRAMMER_ID = ?',
            (first_name, last_name, gender, phone, email, dob, doj, prof1, prof2, salary, programmer_id))
        connection.commit()
        st.success('Record Updated Successfully')


# ******************************
# Delete Operation Function
# ******************************

def delete_record():
    st.subheader('DELETE RECORD FROM PROGRAMMER TABLE')
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID',value=0)
    cursor.execute("SELECT * FROM PROGRAMMER WHERE PROGRAMMER_ID = ?", (programmer_id,))
    existing_record = cursor.fetchone()
    if not existing_record:
        st.error(f"Record with ID {programmer_id} not found. Unable to delete.")
        return
    if st.button('Delete'):
        cursor.execute("DELETE FROM PROGRAMMER WHERE PROGRAMMER_ID = ?", (programmer_id,))
        connection.commit()
        st.success("Record Deleted Successfully")