import sys
from PyQt5 import QtWidgets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from WmUi import Ui_MainWindow  # Import the generated UI class
import mysql.connector
import pandas as pd
###from PyQt5.uic import loadUi


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        ###loadUi("WmUi.ui", self)  # Call setupUi directly
        self.init_ui()  # Call init_ui to connect buttons

    def init_ui(self):
        # Establish connection to MySQL database
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="water_monitoring_system"
        )

        # Create cursor object to execute SQL queries
        self.cursor = self.db_connection.cursor()

        # Connect buttons to functions
        self.pushButton_18.clicked.connect(self.add_complaint)
        self.pushButton_5.clicked.connect(self.add_water_source)
        self.pushButton_4.clicked.connect(self.register_user)
        self.pushButton.clicked.connect(self.export_to_spreadsheet)
        self.pushButton_2.clicked.connect(self.send_warning_emails)

    def fetch_complaint(self):
        try:
            query = "SELECT * FROM `complaints`"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.populate_table(self.tableWidget_8, result)
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def fetch_water_source(self):
        try:
            query = "SELECT * FROM `water_source`"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.populate_table(self.tableWidget_7, result)
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def fetch_user(self):
        try:
            query = "SELECT * FROM `users`"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.populate_table(self.tableWidget, result)
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def populate_table(self, table_widget, data):
        table_widget.setRowCount(0)  # Clear existing rows
        for row_num, row_data in enumerate(data):
            table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                table_widget.setItem(row_num, col_num, item)        
    
    def register_user(self):
        try:
            # Retrieve input data from the fields
            username = self.lineEdit.text()
            email = self.lineEdit_2.text()
            user_type = self.lineEdit_4.text()

            # Define the SQL INSERT statement
            sql = "INSERT INTO users (username, email, user_type) VALUES (%s, %s, %s)"
            values = (username, email, user_type)
        
            # Execute the SQL query
            self.cursor.execute(sql, values)

            # Commit changes to the database
            self.db_connection.commit()

            # Display success message
            QMessageBox.information(self, "Success", "User registered successfully!")

            # Add the new row to the customer table
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for col_num, col_data in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_position, col_num, item)
            self.fetch_user()

        except mysql.connector.Error as error:
            # Display error message
            QMessageBox.critical(self, "Error", f"Failed to register user: {error}")


    def add_water_source(self):
        try:
            # Retrieve input data from the fields
            source_name = self.lineEdit_3.text()
            condition = self.lineEdit_5.text()

            # Define the SQL INSERT statement
            sql = "INSERT INTO water_source (source_name, ondition) VALUES (%s, %s)"
            values = (source_name, condition)

            # Execute the SQL query
            self.cursor.execute(sql, values)

            # Commit changes to the database
            self.db_connection.commit()

            # Display success message
            QMessageBox.information(self, "Success", "Water source added successfully!")

            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)
            for col_num, col_data in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.tableWidget_7.setItem(row_position, col_num, item)
            self.fetch_water_source()    

        except mysql.connector.Error as error:
            # Display error message
            QMessageBox.critical(self, "Error", f"Failed to add water source: {error}")
            

    def add_complaint(self):
        try:
            # Retrieve input data from the fields
            source_id = self.lineEdit_13.text()
            complaint = self.textEdit.toPlainText()

            # Define the SQL INSERT statement
            sql = "INSERT INTO complaints (source_ide, complaint_text) VALUES (%s, %s)"
            values = (source_id, complaint)

            # Execute the SQL query
            self.cursor.execute(sql, values)

            # Commit changes to the database
            self.db_connection.commit()

            # Display success message
            QMessageBox.information(self, "Success", "Complaint added successfully!")

            row_position = self.tableWidget_8.rowCount()
            self.tableWidget_8.insertRow(row_position)
            for col_num, col_data in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.tableWidget_8.setItem(row_position, col_num, item)

            self.fetch_complaint()

        except mysql.connector.Error as error:
            # Display error message
            QMessageBox.critical(self, "Error", f"Failed to add complaint: {error}")

    def export_to_spreadsheet(self):
        try:
            # Query water source information from the database
            sql = "SELECT * FROM water_source"
            self.cursor.execute(sql)
            water_sources = self.cursor.fetchall()

            # Convert the data to a pandas DataFrame
            df = pd.DataFrame(water_sources, columns=["Name", "Status"])

            # Export the DataFrame to a spreadsheet
            file_path = "water_sources.xlsx"
            df.to_excel(file_path, index=False)

            # Display success message
            QMessageBox.information(self, "Success", f"Water source information exported to {file_path}")

        except mysql.connector.Error as error:
            # Display error message
            QMessageBox.critical(self, "Error", f"Failed to export water source information: {error}")

    def send_warning_emails(self):
        try:
            # Query users in danger areas from the database
            sql = "SELECT email FROM users"  # Assuming danger_area is stored as a boolean
            self.cursor.execute(sql)
            users = self.cursor.fetchall()

            # Prepare email content
            subject = "Warning: Danger Area Alert"
            message_body = "This is a warning message regarding the dangerous water conditions in your area. Please take necessary precautions."

            sender_email = "madickangecesar59@gmail.com"  # sender email address
            sender_password = "Madick 12"  # sender email password
            receiver_email = "madick.angecesar@ictuniversity.edu.cm"

            # Set up SMTP server connection
            smtp_server = "smtp.gmail.com"  # Update with your SMTP server
            smtp_port = 587  # Update with your SMTP port
            # Create SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send emails to users
            for user in users:
                receiver_email = user[0]
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message.attach(MIMEText(message_body, "plain"))
                smtp_server.sendmail(sender_email, receiver_email, message.as_string())

            # Close SMTP session
            smtp_server.quit()

            # Display success message
            QMessageBox.information(self, "Success", "Warning emails sent successfully")

        except (mysql.connector.Error, smtplib.SMTPException) as error:
            # Display error message
            QMessageBox.critical(self, "Error", f"Failed to send warning emails: {error}")
            print(self, "Error", f"Failed to send warning emails: {error}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MyApp() 
    main_app.show()
    sys.exit(app.exec_())
