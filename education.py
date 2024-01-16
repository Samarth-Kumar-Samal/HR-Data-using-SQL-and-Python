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
    st.subheader("CREATE A EDUCATION RECORD")
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID OF THE EDUCATION : ',value=0)
    software_id = st.number_input('ENTER THE SOFTWARE ID OF THE EDUCATION : ',value=0)
    institute_name = st.text_input('ENTER THE INSTITUTE NAME OF THE EDUCATION :')
    course_name = st.text_input('ENTER THE COURSE NAME OF THE EDUCATION :')
    course_fee = st.number_input('ENTER THE COURSE FEE OF THE EDUCATION :',value=0)
    
    if st.button('Create'):
        if exist_record(programmer_id, software_id, institute_name, course_name, course_fee):
            st.error('Record Already Exists')
        else:
            cursor.execute(
                'INSERT INTO PROGRAMMER(PROGRAMMER_ID,SOFTWARE_ID,INSTITUTE_NAME,COURSE_NAME,COURSE_FEE) VALUES(?,?,?,?,?)',
                (programmer_id, software_id, institute_name, course_name, course_fee))
            connection.commit()
            st.success('Record Created Successfully')


# ***********************************
# Checking Existing Record Function
# ***********************************

def exist_record(programmer_id, software_id, institute_name, course_name, course_fee):
    cursor.execute(
        'SELECT * FROM EDUCATION WHERE PROGRAMMER_ID = ? AND SOFTWARE_ID = ? AND INSTITUTE_NAME = ? AND COURSE_NAME = ? AND COURSE_FEE = ?',
        (programmer_id, software_id, institute_name, course_name, course_fee))
    existing_record = cursor.fetchone()
    return existing_record is not None


# ******************************
# Reading Operation Function
# ******************************

def read_record():
    st.subheader('READING RECORDS FROM EDUCATION TABLE')
    cursor.execute('SELECT * FROM EDUCATION')
    result = cursor.fetchall()
    columns = [str(column[0]).upper() for column in cursor.description]
    data_with_columns = [columns] + list(result)
    st.table(data_with_columns)

# ******************************
# Update Operation Function
# ******************************

def update_record():
    st.subheader('UPDATE RECORD IN EDUCATION TABLE')
    software_id = st.number_input('ENTER THE SOFTWARE ID :',value=0)
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID :',value=0)
    cursor.execute("SELECT * FROM EDUCATION WHERE SOFTWARE_ID = ? AND PROGRAMMER_ID = ?", (software_id,programmer_id))
    existing_record = cursor.fetchone()

    if not existing_record:
        st.error(f'Record with SOFTWARE ID {software_id} and PROGRAMMER ID {programmer_id} not found. Unable to update.')
        return
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID OF THE EDUCATION : ',value=0)
    software_id = st.number_input('ENTER THE SOFTWARE ID OF THE EDUCATION : ',value=0)
    institute_name = st.text_input('ENTER THE INSTITUTE NAME OF THE EDUCATION :')
    course_name = st.text_input('ENTER THE COURSE NAME OF THE EDUCATION :')
    course_fee = st.number_input('ENTER THE COURSE FEE OF THE EDUCATION :',value=0)
    
    if st.button('Update'):
        cursor.execute(
            'UPDATE SOFTWARE SET PROGRAMMER_ID = ?,SOFTWARE_ID = ?,INSTITUTE_NAME = ?,COURSE_NAME = ?,COURSE_FEE = ? WHERE SOFTWARE_ID = ? AND PROGRAMMER_ID = ?',
            (programmer_id, software_id, institute_name, course_name, course_fee, software_id, programmer_id))
        connection.commit()
        st.success('Record Updated Successfully')


# ******************************
# Delete Operation Function
# ******************************

def delete_record():
    st.subheader('DELETE RECORD FROM EDUCATION TABLE')
    software_id = st.number_input('ENTER THE SOFTWARE ID :',value=0)
    programmer_id = st.number_input('ENTER THE PROGRAMMER ID :',value=0)
    cursor.execute("SELECT * FROM EDUCATION WHERE SOFTWARE_ID = ? AND PROGRAMMER_ID = ?", (software_id,programmer_id))
    existing_record = cursor.fetchone()
    if not existing_record:
        st.error(f"Record with SOFTWARE ID {software_id} AND PROGRAMMER ID {programmer_id} not found. Unable to delete.")
        return
    if st.button('Delete'):
        cursor.execute("DELETE FROM EDUCATION WHERE SOFTWARE_ID = ? AND PROGRAMMER_ID = ?", (software_id,programmer_id))
        connection.commit()
        st.success("Record Deleted Successfully")