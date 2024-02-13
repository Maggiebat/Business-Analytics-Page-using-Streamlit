import mysql.connector
# import streamlit as st

conn=mysql.connector.connect(
  host="localhost",
  port="3306",
  user="root",
  passwd="maggie",
  db="irrelevent"
)

c=conn.cursor()

def view_all_data():
    c.execute('select * from customers order by id asc')
    data = c.fetchall()
    return  data