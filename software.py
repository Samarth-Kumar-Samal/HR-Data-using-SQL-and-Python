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
    st.subheader("CREATE A SOFTWARE RECORD")
    programmer_id = st.number_input('ENTER THE PROGRAMMER_ID OF THE SOFTWARE : ',value=0)
    software_name = st.text_input('ENTER THE SOFTWARE NAME OF THE SOFTWARE : ')
    developed_in = st.text_input('ENTER THE DEVELOPED IN OF THE SOFTWARE :')
    cost_price = st.number_input('ENTER THE COST PRICE OF THE SOFTWARE :',value=0)
    sell_price = st.number_input('ENTER THE SELL PRICE OF THE SOFTWARE :',value=0)
    units = st.number_input('ENTER THE UNITS OF THE SOFTWARE :',min_value=0)

    if st.button('Create'):
        if exist_record(programmer_id, software_name, developed_in, cost_price, sell_price, units):
            st.error('Record Already Exists')
        else:
            cursor.execute(
                'INSERT INTO PROGRAMMER(PROGRAMMER_ID,SOFTWARE_NAME,DEVELOPED_IN,COST_PRICE,SELL_PRICE,UNITS) VALUES(?,?,?,?,?,?)',
                (programmer_id, software_name, developed_in, cost_price, sell_price, units))
            connection.commit()
            st.success('Record Created Successfully')


# ***********************************
# Checking Existing Record Function
# ***********************************

def exist_record(programmer_id,software_name,developed_in,cost_price,sell_price,units):
    cursor.execute(
        'SELECT * FROM PROGRAMMER WHERE PROGRAMMER_ID = ? AND SOFTWARE_NAME = ? AND DEVELOPED_IN = ? AND COST_PRICE = ? AND SELL_PRICE = ? AND UNITS = ?',
        (programmer_id, software_name, developed_in, cost_price, sell_price, units))
    existing_record = cursor.fetchone()
    return existing_record is not None


# ******************************
# Reading Operation Function
# ******************************

def read_record():
    st.subheader('READING RECORDS FROM SOFTWARE TABLE')
    cursor.execute('SELECT * FROM SOFTWARE')
    result = cursor.fetchall()
    columns = [str(column[0]).upper() for column in cursor.description]
    data_with_columns = [columns] + list(result)
    st.table(data_with_columns)

# ******************************
# Update Operation Function
# ******************************

def update_record():
    st.subheader('UPDATE RECORD IN SOFTWARE TABLE')
    software_id = st.number_input('ENTER THE SOFTWARE ID :',value=0)
    cursor.execute("SELECT * FROM SOFTWARE WHERE SOFTWARE_ID = ?", (software_id,))
    existing_record = cursor.fetchone()

    if not existing_record:
        st.error(f'Record with SOFTWARE ID {software_id} not found. Unable to update.')
        return
    programmer_id = st.number_input('ENTER THE PROGRAMMER_ID OF THE SOFTWARE : ',value=0)
    software_name = st.text_input('ENTER THE SOFTWARE NAME OF THE SOFTWARE : ')
    developed_in = st.text_input('ENTER THE DEVELOPED IN OF THE SOFTWARE :')
    cost_price = st.number_input('ENTER THE COST PRICE OF THE SOFTWARE :',value=0)
    sell_price = st.number_input('ENTER THE SELL PRICE OF THE SOFTWARE :',value=0)
    units = st.number_input('ENTER THE UNITS OF THE SOFTWARE :',min_value=0)
    
    if st.button('Update'):
        cursor.execute(
            'UPDATE SOFTWARE SET PROGRAMMER_ID = ?,SOFTWARE_NAME = ?,DEVELOPED_IN = ?,COST_PRICE = ?,SELL_PRICE = ?,UNITS = ? WHERE SOFTWARE_ID = ?',
            (programmer_id, software_name, developed_in, cost_price, sell_price, units, software_id))
        connection.commit()
        st.success('Record Updated Successfully')


# ******************************
# Delete Operation Function
# ******************************

def delete_record():
    st.subheader('DELETE RECORD FROM SOFTWARE TABLE')
    software_id = st.number_input('ENTER THE SOFTWARE ID :',value=0)
    cursor.execute("SELECT * FROM SOFTWARE WHERE SOFTWARE_ID = ?", (software_id,))
    existing_record = cursor.fetchone()
    if not existing_record:
        st.error(f"Record with ID {software_id} not found. Unable to delete.")
        return
    if st.button('Delete'):
        cursor.execute("DELETE FROM SOFTWARE WHERE SOFTWARE_ID = ?", (software_id,))
        connection.commit()
        st.success("Record Deleted Successfully")