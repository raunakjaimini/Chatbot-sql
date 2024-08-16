import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''Insert Into STUDENT values('Raunak','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Karnika','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Aakash','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Yuvraj','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Harsh','DEVOPS','A',35)''')

## Disspaly ALl the records

print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()