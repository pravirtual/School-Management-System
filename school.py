#import all the necessary pyqy5 libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType #for connecting ui to python file
import mysql.connector as con
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

ui,_ = loadUiType('school.ui') #basically loading ui of project into this python file

#basically creating the mainapp class that will load the .ui file in the constructor
class MainApp(QMainWindow,ui):
    def __init__(self): #constructor class
        QMainWindow.__init__(self) #call the superclass constructor method
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)  #set current tab to login form
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.b01.clicked.connect(self.login)
        self.menu11.triggered.connect(self.show_add_new_student_tab)
        self.b11.clicked.connect(self.save_student_details)
        self.menu12.triggered.connect(self.show_edit_student_details_tab)
        self.cb21.currentIndexChanged.connect(self.fill_student_details_when_combobox_selected)
        self.b21.clicked.connect(self.edit_student_details)
        self.b22.clicked.connect(self.delete_student_details)
        self.menu21.triggered.connect(self.show_add_edit_mark_details_tab)
        self.b3l1.clicked.connect(self.save_mark_details)
        self.cb3r1.currentIndexChanged.connect(self.load_mark_details_from_db)
        self.b3r1.clicked.connect(self.edit_mark_details)
        self.b3r2.clicked.connect(self.delete_mark_details)
        self.menu31.triggered.connect(self.show_add_edit_attendance_details_tab)
        self.b4l1.clicked.connect(self.save_attendance_details)
        self.cb4r1.currentIndexChanged.connect(self.load_date_db_attendance_details)
        self.b4r1.clicked.connect(self.fetch_attendance_details_from_db)
        self.b4r2.clicked.connect(self.edit_attendance_details)
        self.b4r3.clicked.connect(self.delete_attendance_details)

        self.menu41.triggered.connect(self.show_add_edit_fees_details_tab)
        self.b5l1.clicked.connect(self.save_fees_details)
        self.cb5r1.currentIndexChanged.connect(self.load_fees_details_when_combobox_selected)
        self.b5r1.clicked.connect(self.edit_fees_details)
        self.b5r2.clicked.connect(self.delete_fees_details)
        self.b81.clicked.connect(self.print_file)
        self.b82.clicked.connect(self.cancel_print)
        self.menu51.triggered.connect(self.show_report)
        self.menu52.triggered.connect(self.show_report)
        self.menu53.triggered.connect(self.show_report)
        self.menu54.triggered.connect(self.show_report)
        self.actionlogout.triggered.connect(self.logout)


    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if(un=="admin" and pw=="admin"):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            self.l01.setText("Invalid admin login details, Try again")
            QMessageBox.information(self,"School Management System","Invalid admin login details, Try again.")

    def show_add_new_student_tab(self):
        self.l11.setText("Enter Student Details")
        self.tb11.clear()
        self.tb12.clear()
        self.tb13.clear()
        self.tb14.clear()
        self.tb15.clear()
        self.tb16.clear()
        self.mtb11.clear()
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()
        
    
    def fill_next_registration_number(self):
        try:
            rn=0
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            # if result:
            for stud in result:
                rn  = int(stud[1]) 
            self.tb11.setText(str(rn+1))
            
        except con.Error as e:
            print("Error occured in select student reg number" + str(e))
    
    def save_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            registration_number = self.tb11.text()
            full_name = self.tb12.text()
            father_name = self.tb13.text()
            gender = self.cb11.currentText()
            date_of_birth = self.tb14.text()
            address = self.mtb11.toPlainText()
            phone = self.tb15.text()
            email = self.tb16.text()
            standard = self.cb12.currentText()

            qry = "insert into student (registration_number, full_name, father_name, gender, date_of_birth, address, phone, email, class) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (registration_number,full_name,father_name,gender,date_of_birth,address,phone,email,standard)
            cursor.execute(qry,value)

            mydb.commit()

            self.l11.setText("Student details saved successfully!")
            QMessageBox.information(self,"School Management System","Student details added successfully")
            self.tabWidget.setCurrentIndex(1)
        
        except con.Error as e:
            self.l11.setText("Error in save student form: " + str(e))
            # print("ERROR is" + str(e))

    
    def show_edit_student_details_tab(self):
        self.l21.setText("Select Student Registration Number")
        self.tb21.clear()
        self.tb22.clear()
        self.tb23.clear()
        self.tb24.clear()
        self.tb25.clear()
        self.tb26.clear()
        self.tb27.clear()
        self.mtb21.clear()
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(3)
        self.load_combobox_reg_no_db()

    def load_combobox_reg_no_db(self):
        try:
            self.cb21.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry = "select * from student"
            cursor.execute(qry)
            result = cursor.fetchall()

            for stud in result:
                self.cb21.addItem(str(stud[1]))

        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def fill_student_details_when_combobox_selected(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry = "select * from student where registration_number='"+ self.cb21.currentText() +"'"
            cursor.execute(qry)
            result = cursor.fetchall()

            for stud in result:
                self.tb21.setText(str(stud[2]))
                self.tb22.setText(str(stud[3]))
                self.tb23.setText(str(stud[4]))
                self.tb24.setText(str(stud[5]))
                self.mtb21.setText(str(stud[6]))
                self.tb25.setText(str(stud[7]))
                self.tb26.setText(str(stud[8]))
                self.tb27.setText(str(stud[9]))

        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")


    def edit_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            registration_number = self.cb21.currentText()
            full_name = self.tb21.text()
            father_name = self.tb22.text()
            gender = self.tb23.text()
            date_of_birth = self.tb24.text()
            address = self.mtb21.toPlainText()
            phone = self.tb25.text()
            email = self.tb26.text()
            standard = self.tb27.text()

            qry = "update student set full_name='"+ full_name +"', father_name='"+ father_name +"', gender='"+ gender +"', date_of_birth='"+ date_of_birth +"', address='"+ address +"', phone='"+ phone +"', email='"+ email +"', class='"+ standard +"' where registration_number='"+ registration_number +"'"
            cursor.execute(qry)

            mydb.commit()

            self.l21.setText("Student details updated successfully!")
            QMessageBox.information(self,"School Management System","Student details updated successfully")
            self.tabWidget.setCurrentIndex(1)
        
        except con.Error as e:
            self.l21.setText("Error in editing student details: " + str(e))
            # print("ERROR is" + str(e))


    def delete_student_details(self):

        m = QMessageBox.question(self,"Delete","Are you sure you want to delete details", QMessageBox.Yes | QMessageBox.No)
        if(m == QMessageBox.Yes):
            try:
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()

                registration_number = self.cb21.currentText()
                qry = "delete from student where registration_number='"+ registration_number +"'"
                cursor.execute(qry)
                mydb.commit()

                self.l21.setText("Student details deleted successfully!")
                QMessageBox.information(self,"School Management System", "Student details deleted successfully")
                self.tabWidget.setCurrentIndex(1)

            except con.Error as e:
                self.l21.setText("Error in deleting student details" + str(e))


############ Mark Details ##############

    def show_add_edit_mark_details_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.l3l1.setText("Enter Marks")
        self.l3r1.setText("Select Registration Number")
        self.tb3l1.clear()
        self.tb3l2.clear()
        self.tb3l3.clear()
        self.tb3l4.clear()
        self.tb3r1.clear()
        self.tb3r2.clear()
        self.tb3r3.clear()
        self.tb3r4.clear()
        self.load_combobox_reg_no_db_mark_details_left()
        self.load_combobox_reg_no_db_mark_details_right()

    def load_combobox_reg_no_db_mark_details_left(self):
        try:
            self.cb3l1.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry1 = "select * from student order by registration_number"
            cursor.execute(qry1)
            result1 = cursor.fetchall()
            for stud in result1:
                self.cb3l1.addItem(str(stud[1]))
        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def load_combobox_reg_no_db_mark_details_right(self):
        try:
            self.cb3r1.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry2="select * from mark order by registration_number"
            cursor.execute(qry2)
            result2 = cursor.fetchall()
            for stud in result2:
                self.cb3r1.addItem(str(stud[1]))
        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")         

    def save_mark_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            
            registration_number = self.cb3l1.currentText()

            cursor.execute("select * from mark")

            result = cursor.fetchall()

            flag=0

            for stud in result:
                if(stud[1] == registration_number):
                    flag=1
                    break
            
            if flag == 1:
                QMessageBox.information(self,"School Management System", "Mark Details of this student is already saved")
            
            else:
                english = self.tb3l1.text()
                maths = self.tb3l2.text()
                science = self.tb3l3.text()
                social_science = self.tb3l4.text()


                qry = "insert into mark (registration_number, english, maths, science, social_science) values(%s,%s,%s,%s,%s)"
                value = (registration_number,english,maths,science,social_science)
                cursor.execute(qry,value)

                mydb.commit()

                self.l3l1.setText("Mark details saved successfully!")
                QMessageBox.information(self,"School Management System","Mark details added successfully")
                self.tabWidget.setCurrentIndex(1)
            
            self.load_combobox_reg_no_db_mark_details_right()
            #self.load_mark_details_from_db()
        
        except con.Error as e:
            self.l3l1.setText("Error in mark form: " + str(e))
            # print("ERROR is" + str(e))

    
    def edit_mark_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()         

            registration_number = self.cb3r1.currentText()
            english = self.tb3r1.text()
            maths = self.tb3r2.text()
            science = self.tb3r3.text()
            social_science = self.tb3r4.text()
            
            qry2 = ("update mark set english='"+ english +"', maths='"+ maths +"', science='"+ science +"', social_science='"+ social_science +"' where registration_number='"+ registration_number +"'")
            cursor.execute(qry2)
            mydb.commit()

            self.l3r1.setText("Mark details updated successfully!")
            QMessageBox.information(self,"School Management System","Mark details updated successfully")
            self.tabWidget.setCurrentIndex(1)


        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def load_mark_details_from_db(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()

            registration_number = self.cb3r1.currentText()
            qry1 = ("select * from mark where registration_number='"+ registration_number +"'")
            cursor.execute(qry1)

            result = cursor.fetchall()

            for stud in result:
                self.tb3r1.setText(str(stud[2]))
                self.tb3r2.setText(str(stud[3]))
                self.tb3r3.setText(str(stud[4]))
                self.tb3r4.setText(str(stud[5]))

        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")


    def delete_mark_details(self):

        m = QMessageBox.question(self,"Delete","Are you sure you want to delete details", QMessageBox.Yes | QMessageBox.No)
        if(m == QMessageBox.Yes):
            try:
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()

                registration_number = self.cb3r1.currentText()
                qry = "delete from mark where registration_number='"+ registration_number +"'"
                cursor.execute(qry)
                mydb.commit()

                # self.clear_text_box_edit_mark_details()

                self.l3r1.setText("Mark details deleted successfully!")
                QMessageBox.information(self,"School Management System", "Mark details deleted successfully")
                self.tabWidget.setCurrentIndex(1)

                

            except con.Error as e:
                self.l3r1.setText("Error in deleting student details" + str(e))

####### ATTENDANCE DETAILS #######

    def show_add_edit_attendance_details_tab(self):
        self.tabWidget.setCurrentIndex(5)
        self.l4l1.setText("Enter Attendance Details")
        self.l4r1.setText("Select Reg. No. and Date")
        self.tb4l1.clear()
        self.tb4l2.clear()
        self.tb4l3.clear()
        self.cb4r2.clear()
        self.tb4r1.clear()
        self.tb4r2.clear()
        
        
        self.load_combobox_reg_no_db_attendance_details_left()
        self.load_combobox_reg_no_db_attendance_details_right()
        self.load_date_db_attendance_details()

    def load_combobox_reg_no_db_attendance_details_left(self):
        try:
            self.cb4l1.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry1 = "select * from student order by registration_number"
            cursor.execute(qry1)
            result1 = cursor.fetchall()
            for stud in result1:
                self.cb4l1.addItem(str(stud[1]))
        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def load_combobox_reg_no_db_attendance_details_right(self):
        try:
            self.cb4r1.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry2="select distinct(registration_number) from attendance order by registration_number"
            cursor.execute(qry2)
            result2 = cursor.fetchall()
            for stud in result2:
                self.cb4r1.addItem(str(stud[0]))

            # self.load_date_db_attendance_details()
        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again") 

    def save_attendance_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            
            registration_number = self.cb4l1.currentText()
            attendance_date = self.tb4l1.text()

            cursor.execute("select * from attendance")

            result = cursor.fetchall()

            flag=0

            for stud in result:
                if(stud[1] == registration_number and stud[2] == attendance_date):
                    flag=1
                    break
            
            if flag == 1:
                QMessageBox.information(self,"School Management System", "Attendance Details of this student for '"+ attendance_date +"' is already saved")
            
            else:
                attendance_date = self.tb4l1.text()
                morning = self.tb4l2.text()
                afteroon = self.tb4l3.text()


                qry = "insert into attendance (registration_number, attendance_date, morning, afternoon) values(%s,%s,%s,%s)"
                value = (registration_number,attendance_date,morning,afteroon)
                cursor.execute(qry,value)

                mydb.commit()

                self.l4l1.setText("Attendance details saved successfully!")
                QMessageBox.information(self,"School Management System","Attendance details added successfully")
                self.tabWidget.setCurrentIndex(1)
            
            self.load_combobox_reg_no_db_attendance_details_right()
            
            #self.load_mark_details_from_db()
        
        except con.Error as e:
            self.l4l1.setText("Error in attendance form: " + str(e))
            # print("ERROR is" + str(e))

    def load_date_db_attendance_details(self):
        try:
            self.cb4r2.clear()
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            registration_number = self.cb4r1.currentText()
            qry = ("select attendance_date from attendance where registration_number='"+ registration_number +"' order by attendance_date")
            cursor.execute(qry)
            result = cursor.fetchall()

            for stud in result:
                self.cb4r2.addItem(str(stud[0]))

        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def fetch_attendance_details_from_db(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()

            registration_number = self.cb4r1.currentText()
            attendance_date = self.cb4r2.currentText()
            qry=("select morning, afternoon from attendance where registration_number='"+ registration_number +"' and attendance_date='"+ attendance_date +"'")
            cursor.execute(qry)
            result = cursor.fetchall()

            self.tb4r1.setText(str(result[0][0]))
            self.tb4r2.setText(str(result[0][1]))

        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")

    def edit_attendance_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()         

            registration_number = self.cb4r1.currentText()
            attendance_date = self.cb4r2.currentText()
            morning = self.tb4r1.text()
            afternoon = self.tb4r2.text()
            
            qry2 = ("update attendance set morning='"+ morning +"', afternoon='"+ afternoon +"' where registration_number='"+ registration_number +"' and attendance_date='"+ attendance_date +"'")
            cursor.execute(qry2)
            mydb.commit()

            self.l4r1.setText("Attendance details updated successfully!")
            QMessageBox.information(self,"School Management System","Attendance details updated successfully")
            self.tabWidget.setCurrentIndex(1)


        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")
    
    def delete_attendance_details(self):

        m = QMessageBox.question(self,"Delete","Are you sure you want to delete details", QMessageBox.Yes | QMessageBox.No)
        if(m == QMessageBox.Yes):
            try:
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()

                registration_number = self.cb4r1.currentText()
                attendance_date = self.cb4r2.currentText()
                qry = "delete from attendance where registration_number='"+ registration_number +"' and attendance_date='"+ attendance_date +"'"
                cursor.execute(qry)
                mydb.commit()

                # self.clear_text_box_edit_mark_details()

                self.l4r1.setText("Attendance details deleted successfully!")
                QMessageBox.information(self,"School Management System", "Attendance details deleted successfully")
                self.tabWidget.setCurrentIndex(1)

                

            except con.Error as e:
                self.l4r1.setText("Error in deleting attendance details" + str(e))

########## FEES DETAILS ########### 
    def show_add_edit_fees_details_tab(self):
        self.tabWidget.setCurrentIndex(6)
        self.l5l1.setText("Enter Fee Details")
        self.l5r1.setText("Select Receipt Number")
        self.tb5l1.clear()
        self.cb5l1.clear()
        self.tb5l2.clear()
        self.tb5l3.clear()
        self.tb5l4.clear()
        self.cb5r1.clear()
        self.tb5r1.clear()
        self.tb5r2.clear()
        self.tb5r3.clear()
        self.tb5r4.clear()
        self.load_reg_no_in_fees_tab()
        self.load_receipt_no_in_fees_tab()
        self.fill_next_receipt_number()

    def load_reg_no_in_fees_tab(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry = "select registration_number from student order by registration_number"
            cursor.execute(qry)
            result = cursor.fetchall()
            for stud in result:
                self.cb5l1.addItem(str(stud[0]))
        
        except:
            QMessageBox.information(self,"School Management System", "Some error occured, try again!")

    def load_receipt_no_in_fees_tab(self):
        try:
            self.cb5r1.clear()
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry = "select receipt_number from fees"
            cursor.execute(qry)
            result = cursor.fetchall()
            for stud in result:
                self.cb5r1.addItem(str(stud[0]))
        
        except:
            QMessageBox.information(self,"School Management System", "Some error occured, try again!")

    def fill_next_receipt_number(self):
        try:
            rn = 0
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            qry = "select receipt_number from fees"
            cursor.execute(qry)
            result = cursor.fetchall()
            for stud in result:
                rn = int(stud[0])

            self.tb5l1.setText(str(rn+1))
        
        except:
            QMessageBox.information(self,"School Management System", "Some error occured, try again!")

    
    
    def load_fees_details_when_combobox_selected(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            receipt_number = self.cb5r1.currentText()
            qry = "select * from fees where receipt_number='"+ receipt_number +"'"
            cursor.execute(qry)
            result = cursor.fetchall()

            for stud in result:
                self.tb5r1.setText(str(stud[2]))
                self.tb5r2.setText(str(stud[3]))
                self.tb5r3.setText(str(stud[4]))
                self.tb5r4.setText(str(stud[5]))
                  
        except:
            QMessageBox.information(self,"School Management System", "Some error occured, try again!")

    
    def save_fees_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()
            receipt_number = self.tb5l1.text()
            registration_number = self.cb5l1.currentText()
            purpose = self.tb5l2.text()
            amount = self.tb5l3.text()
            fees_date = self.tb5l4.text()

            qry = "insert into fees (receipt_number, registration_number, purpose, amount, fees_date) values(%s,%s,%s,%s,%s)"
            value = receipt_number,registration_number, purpose, amount, fees_date
            cursor.execute(qry, value)
            mydb.commit()
            
            self.l5l1.setText("Fees details added successfully!")
            QMessageBox.information(self,"School Management System","Fees details added successfully!")
            self.load_receipt_no_in_fees_tab()        

            self.l81.setText(self.tb5l1.text())
            self.l82.setText(self.tb5l4.text())
            self.l84.setText(self.tb5l3.text())
            self.l85.setText(self.tb5l2.text())
            self.l86.setText(self.tb5l4.text())
            cursor.execute("select full_name from student where registration_number='"+ registration_number +"'")
            result = cursor.fetchone()
            self.l83.setText(str(result[0]))
            self.tabWidget.setCurrentIndex(8)

        except:
            QMessageBox.information(self,"School Management System", "Some error occured, try again!")

    
    
    def edit_fees_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="", db="school")
            cursor = mydb.cursor()         

            receipt_number = self.cb5r1.currentText()
            registration_number = self.tb5r1.text()
            purpose = self.tb5r2.text()
            amount = self.tb5r3.text()
            fees_date = self.tb5r4.text()
            
            qry = ("update fees set registration_number='"+ registration_number +"', purpose='"+ purpose +"', amount='"+ amount +"', fees_date='"+ fees_date +"' where receipt_number='"+ receipt_number +"'")
            cursor.execute(qry)
            mydb.commit()

            self.l5r1.setText("Fees Details updated successfully!")
            QMessageBox.information(self,"School Management System","Fees details updated successfully")
            self.tabWidget.setCurrentIndex(1)


        except con.Error as e:
            QMessageBox.information(self,"School Management System","some error occured, Try again")
    
    def delete_fees_details(self):

        m = QMessageBox.question(self,"Delete","Are you sure you want to delete details", QMessageBox.Yes | QMessageBox.No)
        if(m == QMessageBox.Yes):
            try:
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()

                receipt_number = self.cb5r1.currentText()
                qry = "delete from fees where receipt_number='"+ receipt_number +"'"
                cursor.execute(qry)
                mydb.commit()

                # self.clear_text_box_edit_mark_details()

                self.l5r1.setText("Fees details deleted successfully!")
                QMessageBox.information(self,"School Management System", "Fees details deleted successfully")
                self.tabWidget.setCurrentIndex(1)

            except con.Error as e:
                self.l4r1.setText("Error in deleting attendance details" + str(e))


######### print fees receipt function ########
    def print_file(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer,self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.tabWidget.print_(printer)


    def cancel_print(self):
        self.tabWidget.setCurrentIndex(1)

###### REPORT FORM ######

    def show_report(self):
        table_name = self.sender()
        self.l61.setText(table_name.text())
        self.tabWidget.setCurrentIndex(7)
        try:
            self.tableReport.setRowCount(0)
            if table_name.text() == "Student Report":
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()
                qry = "select registration_number,full_name,father_name,gender,date_of_birth,address,phone,email,class from student"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number, row_data in enumerate(result):
                    r += 1
                    c = 0
                    for column_number, data in enumerate(row_data):
                        c += 1
                self.tableReport.clear()
                self.tableReport.setColumnCount(c)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number,QTableWidgetItem(str(data)))
                
                #to display heading of the columns
                self.tableReport.setHorizontalHeaderLabels(['Reg Number','Name','Father Name','Gender','Date of Birth','Address','Phone','Email','Class'])
            
            elif table_name.text() == "Marks Report":
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()
                qry = "select registration_number,english,maths,science,social_science from mark"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number, row_data in enumerate(result):
                    r += 1
                    c = 0
                    for column_number, data in enumerate(row_data):
                        c += 1
                self.tableReport.clear()
                self.tableReport.setColumnCount(c)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
                #to display heading of the columns
                self.tableReport.setHorizontalHeaderLabels(['Reg Number','English','Maths','Science','Social Science'])

            elif table_name.text() == "Attendance Report":
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()
                qry = "select registration_number, attendance_date, morning, afternoon from attendance"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number, row_data in enumerate(result):
                    r += 1
                    c = 0
                    for column_number, data in enumerate(row_data):
                        c += 1
                self.tableReport.clear()
                self.tableReport.setColumnCount(c)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
                #to display heading of the columns
                self.tableReport.setHorizontalHeaderLabels(['Reg Number','Date','Morning','Afternoon'])
            
            elif table_name.text() == "Fee Report":
                mydb = con.connect(host="localhost", user="root", password="", db="school")
                cursor = mydb.cursor()
                qry = "select receipt_number, registration_number, purpose, amount, fees_date from fees"
                cursor.execute(qry)
                result = cursor.fetchall()
                r = 0
                c = 0
                for row_number, row_data in enumerate(result):
                    r += 1
                    c = 0
                    for column_number, data in enumerate(row_data):
                        c += 1
                self.tableReport.clear()
                self.tableReport.setColumnCount(c)
                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
                #to display heading of the columns
                self.tableReport.setHorizontalHeaderLabels(['Receipt No.','Reg Number','Purpose','Amount','Date'])

        except con.Error as e:
            print(str(e))
            
    def logout(self):
        #self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.tb01.clear()
        self.tb02.clear()
        self.tabWidget.setCurrentIndex(0)
        QMessageBox.information(self,"School Management System", "You logged out successfully!")


        
def main():
    app = QApplication(sys.argv) #created object of QApplication
    window = MainApp()  #created object of MainApp
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()