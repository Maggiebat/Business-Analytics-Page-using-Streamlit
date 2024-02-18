import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards


# import sql database
from mysql_con import *

st.set_page_config("Business Amalytics Dashboard", page_icon="", layout="wide")
st.subheader("Business Analystics Dashboard")

# call css file
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# process data from query
result = view_all_data()
result2 = viewASS()

# setting the DataFrame
df = pd.DataFrame(result, columns=["EEID", "FullName","JobTitle", "Department", "BusinessUnit", "Gender", "Ethnicity", "Age", "HireDate", "AnnualSalary", "Bonus", "Country", "City", "id"])
df2 = pd.DataFrame(result2, columns=["department", "annualsum", "ID"])

# this will show the entire dataframe
# st.dataframe(df)

# the side bar
st.sidebar.header('Filter Department')
Department=st.sidebar.multiselect(
    label="Filter Department",
    options= df["Department"].unique(),
    default= df["Department"].unique(),
)

st.sidebar.header('Filter Country')
Country=st.sidebar.multiselect(
    label="Filter Country",
    options= df["Country"].unique(),
    default= df["Country"].unique(),
)

st.sidebar.header('Filter Business Unit')
BusinessUnit=st.sidebar.multiselect(
    label="Filter Business Unit",
    options= df["BusinessUnit"].unique(),
    default= df["BusinessUnit"].unique(),
)

st.sidebar.header('Filter Department ASS')
department=st.sidebar.multiselect(
    label="Filter Department ASS",
    options= df2["department"].unique(),
    default= df2["department"].unique(),
)

# process the query
df_selection=df.query(
    "Department==@Department & Country==@Country & BusinessUnit==@BusinessUnit"
)

df_selection2=df2.query(
    "department==@department"
)

# making the cards
def metrics():
    col1,col2,col3=st.columns(3)
    col1.metric("Total Customers", value=df_selection.id.count(), delta="All Customers")
    col2.metric("Annual Salary", value= f"{df_selection2.annualsum.sum():,.0f}",delta="Annual Salary Total")
    col3.metric("Max Salary", value=f"{df_selection2.annualsum.max():,.0f}",delta="Highest Salary")
    
    style_metric_cards (
        background_color="#ffffff", border_left_color="#ff4b4b",
    )

def metrics2():
    # check the populated department thing
    col1,col2=st.columns(2)
    col1.metric("Average Age", value=f"{df_selection.Age.mean():.0f}",delta="Average Age")
    col2.metric("Most Populated Department", value=df_selection.Department.max(),delta="Most Populated Department")


#metrics()

div1, div2 = st.columns(2)

# making the pie chart
def pie():
    with div1:
        theme_plotly=None
        fig=px.pie(df_selection,values="AnnualSalary", names="Department", title="Customer by Department")
        fig.update_layout(legend_title='Department', legend_y=0.9)
        fig.update_traces(textinfo="percent + label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True,theme=theme_plotly)

#pie()

# making the bar chart
def bar():
    with div2:
        theme_plotly=None
        fig=px.bar(df_selection, y="AnnualSalary", x="Department", text_auto="0.2s", title="Annual Salary by Department")
        fig.update_traces(textfont_size=1, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly) 

def newbar():
    with div2:
        theme_plotly=None
        fig=px.bar(df_selection2, y="annualsum", x="department", text_auto="0.2s", title="Annual Salary by Department")
        fig.update_traces(textfont_size=1, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly) 

#bar()
        
def sunburst():
    # attach to the sidebar
    theme_plotly=None
    fig=px.sunburst(df, path=["Gender", "Department", "Ethnicity"])
    # have it show the average salary when you hover over it (average f)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)  
    
def icicle():
    # not being used
    with div2:
        theme_plotly=None
        fig = px.icicle(df, path=[px.Constant("all"), 'Gender', "Ethnicity", "Department"])
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def bubble():
    # attach to sidebar
    with div2:
        theme_plotly=None
        # should y be salary, or bonus
        # should x be age or salary
        fig=px.scatter(df, x="Age", y="AnnualSalary", color="Department", log_x=True, hover_name="FullName")
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def geoMap():
    # this map shows the map of where the people are
    # need to show the amount of people in each country
    theme_plotly=None
    fig=px.scatter_geo(df, color="City", hover_name="Country")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# making the table
def table():
    with st.expander("My Database Table", expanded=True):
        showdata=st.multiselect("Filter Dataset", df_selection.columns, default=["EEID", "FullName","JobTitle", "Department", "BusinessUnit", "Gender", "Ethnicity", "Age", "HireDate", "AnnualSalary", "Bonus", "Country", "City", "id"])
        st.dataframe(df_selection[showdata], use_container_width=True)

#table()

def table2():
    with st.expander("My Database Table", expanded=True):
        showdata=st.multiselect("Filter Dataset", df_selection2.columns, default=["department", "annualsum", "ID"])
        st.dataframe(df_selection2[showdata], use_container_width=True)

# side navigation
with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home", "Table", "AnnualSalary"],
        icons=["house", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

# insert into annualsalarysum(IT) select SUM(customers.AnnualSalary) from customers where Department='IT'
# above is a SQL statement to put the annual salaries sum into a new table

if selected=="Home":
    sunburst()
    pie()
    bubble()
    geoMap()
    metrics2()
elif selected=="Table":
    table()
    df_selection
elif selected=="AnnualSalary":
    with div1:
        table2()
    newbar()
    metrics()
    df_selection2.describe().T
