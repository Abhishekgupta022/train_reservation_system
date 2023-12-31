from random import randint
from datetime import datetime, timedelta
import calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
from email_validator import validate_email, EmailNotValidError
import csv
import mysql.connector

users = {}
mob: int
gender: str
mobile: str
file_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\vs code C\\Python\\station_name_code.csv"

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='user_signup_data'
)


class TicketBooking:
    def select_boarding_details(self):
        print("Enter Only Station_code for TicketBooking")
        while True:
            self.boarding = input("Enter the Boarding Point: ").strip()
            self.destination = input("Enter the Destination Point: ").strip()
            if self.boarding == self.destination:
                print("Boarding and destination cannot be the same. Please try again.\n")
                continue

            with open(file_path, mode='r') as file:
                read_csv = csv.reader(file)
                found_b = False
                found_d = False

                for line in read_csv:
                    if self.boarding == line[2]:
                        print(f"Boarding: {line[0]} ({self.boarding})")
                        found_b = True

                    if self.destination == line[3]:
                        print(f"Destination: {line[0]} ({self.destination})")
                        found_d = True

                    if found_b and found_d:
                        return self.boarding, self.destination  # Return the values as a tuple

                print("At least one of the stations is not available. Please try again.\n")

    def __init__(self):
        self.quota_options = ['General', 'Sleeper', '3AC', '2AC', '1AC']
        self.boarding = self.passengers = self.destination = None
        self.passenger_count = 0
        self.selected_quota = self.date_str = self.email_id = self.total_fare = None

        
        self.seat_details = self.generate_seat_details()
        self.pnr = self.generate_pnr()

    def display_quota_options(self):
        for ind, quota in enumerate(self.quota_options):
            return ('{}: {}'.format(ind + 1, quota))

    def select_quota(self):
        choice = input("Enter the corresponding number for the quota: ")
        choice = int(choice)
        if 1 <= choice <= len(self.quota_options):

            selected_quota = self.quota_options[choice - 1]
            self.selected_quota = selected_quota
            print("You selected: {}".format(selected_quota))
            return selected_quota
        else:
            print("Select the Quota Again!! ")
            return self.select_quota()

    def select_date(self):
        today = datetime.now().date()
        future_limit = today + timedelta(days=4 * 30)  # Limit to 4 months in the future

        while True:
            date_str = input("Enter the date (YYYY-MM-DD): ")
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                self.date_str = selected_date.strftime("%Y-%m-%d")
                day = selected_date.weekday()
                if today <= selected_date <= future_limit:
                    print("You selected:", selected_date)
                    return selected_date, calendar.day_name[day]
                else:
                    raise ValueError("Selected date is out of range")
            except ValueError:
                print("Invalid date. Please enter a date between {} and {}".format(today, future_limit))

    def generate_seat_details(self):
        seat_details = {
            'General': {
                'coach': 'GN',
                'total_coaches': 2,
                'seat_range': (1, 80)
            },
            'Sleeper': {
                'coach': 'S',
                'total_coaches': 13,
                'seat_range': (1, 72)
            },
            '3AC': {
                'coach': 'B',
                'total_coaches': 6,
                'seat_range': (1, 72)
            },
            '2AC': {
                'coach': 'A',
                'total_coaches': 4,
                'seat_range': (1, 54)
            },
            '1AC': {
                'coach': 'H',
                'total_coaches': 2,
                'seat_range': (1, 24)
            }
        }
        return seat_details

    def calculate_fare(self, quota):
        if quota == 'General':
            fare = randint(55, 350)
        elif quota == 'Sleeper':
            fare = randint(300, 800)
        elif quota == '3AC':
            fare = randint(1000, 2100)
        elif quota == '2AC':
            fare = randint(1100, 3500)
        elif quota == '1AC':
            fare = randint(1200, 4800)
        else:
            raise ValueError("Invalid quota selected")

        return fare

    def book_tickets(self):
        while True:
            passenger_count = input("Enter the number of passengers: ")

            try:
                passenger_count = int(passenger_count)
            except ValueError:
                print("Enter Integer not String")
                continue

            if passenger_count <= 0:
                print("Passenger count must be greater than 0")
                continue
            elif passenger_count >= 7:
                print("Maximum Allowable on One Time Booking is 6")
                continue
            else:
                break
        selected_quota = self.select_quota()
        selected_date, day = self.select_date()

        self.passengers = [{}] * passenger_count
        self.boarding, self.destination = self.select_boarding_details()

        for i in range(passenger_count):
            passenger = self.get_passenger_info(i + 1, selected_quota)
            self.passengers[i] = passenger
        #             self.passengers.append(passenger)

        #         smtp_username = getpass.getpass("SMTP Username: ")
        smtp_username = 'reservation.cystum@gmail.com'
        #         smtp_password = getpass.getpass("SMTP Password: ")
        smtp_password = 'dijeocfyweumpgam'
        # email_id = input("Enter the Email ID for receiving the ticket details: ")
        while True:
            try:
                self.email_id = input("Enter the Email ID for receiving the ticket details:  ")
                email_id = self.email_id
                validate_email(email_id)
                break
            except EmailNotValidError:
                print("Invalid email address! Please enter a valid email.")
        self.send_email(self.passengers, self.boarding, self.destination, selected_date, day, email_id, smtp_username,
                        smtp_password)

    def get_passenger_info(self, i, selected_quota):
        global mob

        passenger_info = {
            'name'   : None,
            'gender' : None,
            'age'    : None,
            'phone'  : None,
            'address': None,
            'seat'   : None,
            'pnr'    : None,
            'fare'   : 0.0,  # Set the initial fare to 0.0
            'status' : None

        }
        name = input("Enter the Name of Passenger {}: ".format(i))
        print("Select passenger {} Gender".format(i))
        gender_options = ['M', 'F', 'T']
        for idx, option in enumerate(gender_options):
            print("{}: {}".format(idx + 1, option))

        while True:
            choice = input("Enter the corresponding number for the gender: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(gender_options):
                    selected_gender = gender_options[choice - 1]
                    print("You selected: {}".format(selected_gender))
                    break
                else:
                    print("Invalid choice! Select the Gender Again.\n")
            else:
                print("Invalid input! Enter a numeric choice.\n")

        while True:
            try:
                age = input('Enter the age of passenger {}: '.format(i))
                if age.isdigit() and 5 < int(age) <= 75:
                    age = int(age)
                    break
                elif age.isdigit() and int(age) <= 5:
                    print("You are Travelling With Child\nKindly Contact with 138 in any emergency")
                    break
                elif age.isdigit() and 100 > int(age) > 75:
                    print("You are Travelling With Old Man\nKindly Contact with 138 in any emergency")
                    break
                else:
                    continue

            except ValueError:
                print("Invalid input! Enter a numeric age.\n")

        mobile = input("Enter User Mobile : ")
        validated_mobile = check_mobile(mobile)
        print(f"User Validated mobile: +91-{validated_mobile}" )
        address = input("Enter the passenger {} address: ".format(i))

        quota = self.quota_options.index(selected_quota)
        seat_details = self.seat_details[self.quota_options[quota]]
        coach_number = randint(1, seat_details['total_coaches'])
        seat_number = i
        seat = "{}{}:{}".format(seat_details['coach'], coach_number, seat_number)
        status = 'CNF'

        if i == 1:
            fare = self.calculate_fare(selected_quota)
        else:
            fare = self.passengers[0]['fare']
        passenger_info.update({
            'name'    : name,
            'gender'  : selected_gender,
            'age'     : age,
            'phone'   : mobile,
            'address' : address,
            'seat'    : seat,
            'pnr'     : self.pnr,
            'fare'    : fare,
            'status'  : status
        })
        return passenger_info

    @staticmethod
    def generate_pnr():
        pnr = randint(10 ** 10, (10 ** 11) - 1)
        return pnr

    def calculate_total_fare(self):
        self.total_fare = sum(passenger['fare'] for passenger in self.passengers)
        total_fare = self.total_fare
        return total_fare

    def print_tickets(self):
        print("Ticket Information:")
        for passenger in self.passengers:
            print("----*----*----*----*----*----*----*----")
            print("Passenger Name: " + passenger['name'])
            print("Gender: " + passenger['gender'])
            print("Age: " + str(passenger['age']))
            print("Phone Number: " + str(passenger['phone']))
            print("Address: " + str(passenger['address']))
            print("Seat: " + str(passenger['seat']))
            print("PNR: " + str(passenger['pnr']))
            print("Fare: " + str(passenger['fare']))
            print("Status: " + str(passenger['status']))
            print("----*----*----*----*----*----*----*----")

        total_fare = self.calculate_total_fare()
        print("Total Fare: Rs.", total_fare)

    def send_email(self, passengers, boarding, destination, selected_date, day, email_id, smtp_username, smtp_password):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'reservation.cystum@gmail.com'

        message = MIMEText('', 'html')
        message['Subject'] = 'Ticket Booking Confirmation'
        message['From'] = sender_email
        email_content = "<html><body>"
        email_content += "<h2>Dear Passenger, your ticket details for the journey from \
         <strong>{}</strong> to <strong>{}</strong> :</h2>".format(
            boarding, destination)
        email_content += "<h3>Date Of Journey: <strong>{} ({})</strong></h3>".format(selected_date, day)
        email_content += f"<table border='1' cellpadding='5'>"
        #         email_content += "<br>"

        for passenger in passengers:
            if 'name' in passenger:
                email_content += "<tr>"
                email_content += "<td>Passenger Name: <b>{}</b></td>".format(passenger['name'])
                email_content += "<td>Gender: <b>{}</b></td>".format(passenger['gender'])
                email_content += "<td>Age: <b>{}</b></td>".format(str(passenger['age']))
                email_content += "<td>Phone Number: <b>{}</b></td>".format(str(passenger['phone']))
                email_content += "<td>Address: <b>{}</b></td>".format(str(passenger['address']))
                email_content += "<td>Seat: <b>{}</b></td>".format(str(passenger['seat']))
                email_content += "<td>PNR: <b>{}</b></td>".format(str(passenger['pnr']))
                email_content += "<td>Fare: <b>{}</b></td>".format(str(passenger['fare']))
                email_content += "<td>Status: <b><span style='color: green;'>{}</span>\
                </b></td>".format(str(passenger['status']))
                email_content += "</tr>"
        email_content += "</body></html>"
        total_fare = self.calculate_total_fare()
        email_content += "<p>Total Fare: Rs. <b>{}</b></p>".format(total_fare)
        email_content += "<h3><span style : 'color': 'blue;'>Happy Journey: INDIAN RAILWAYS</h3>"
        message.set_payload(email_content)
        message['To'] = email_id
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
def check_mobile(mobile):
        valid_mob = False
        while not valid_mob:        
            if len(mobile) == 10 and mobile.isdigit() and mobile[0] != '0':
                valid_mob = True
                return mobile
            else:
                print("Invalid phone number!\nPhone number must be without the country code and does not start with 0.\n")
                mobile = input("Enter User Mobile : ")

def calculate_age(dob):
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def signup():
    global gender, mobile
    print("Please fill out the following signup form:")
    name = input("Enter Full Name: ")
    print("Select User Gender!!")
    gender_options = ['M', 'F', 'T']
    for idx, option in enumerate(gender_options):
        print("{}: {}".format(idx + 1, option))

    while True:
        gender_choice = input("Enter the corresponding number for Gender: ")
        try:
            gender_choice = int(gender_choice)
            if 1 <= gender_choice <= len(gender_options):
                gender = gender_options[gender_choice - 1]
                break
            else:
                print("Select Gender Again")
                continue
        except ValueError:
            print("Invalid choice for Gender! Please try again.")
    while True:
        dob_str = input("User Date of Birth (YYYY-MM-DD): ")
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            age = calculate_age(dob)
            if age < 18:
                print("You must be at least 18 years old to create an account.")
            elif age > 90:
                print("Too OLD for creating UserID")
            else:
                break
        except ValueError:
            print("Invalid date format! Please enter the date in the format YYYY-MM-DD.")

    mobile = input("Enter User Mobile : ")
    validated_mobile = check_mobile(mobile)
    print(f"User Validated mobile: +91-{validated_mobile}" )

    while True:
        try:
            email = input("User Email_Id: ")
            validate_email(email)
            break
        except EmailNotValidError:
            print("Invalid email address! Please enter a valid email.")
    address = input("User Permanent Address: ")
    cursor = db_connection.cursor()
    exist_user = """SELECT username from users """
    cursor.execute(exist_user)
    existing_usernames = [row[0] for row in cursor.fetchall()]
    while True:
        try:
            username = input("Create Username: ")
            if len(username)>10:
                print("Enter username less than 10 characters")
                continue
            else:
                print("Yay Username Criteria Satisfied!!")
                break
        except ValueError:
            print("Username less than 10 characters")
            
        
        
        

        if username in existing_usernames:
            print("USER EXISTS!!")
        else:
            print(f"USERNAME {username} AVAILABLE")
            break
    cursor.close()
#     db_connection.close()

    password = getpass.getpass("Create Password: ")
    users[username] = {
        'name': name,
        'gender': gender,
        'age': age,
        'mobile': mobile,
        'email': email,
        'address': address,
        'password': password
    }

    # Send a prompt email to the user
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'reservation.cystum@gmail.com'
    #     sender_email = getpass.getpass("SMTP Username: ")
    #     sender_password = getpass.getpass("SMTP Password: ")
    sender_password = 'dijeocfyweumpgam'
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Signup Confirmation'
    message['From'] = sender_email
    message['To'] = email
    text_content = "Signup Successful! Your username is: {} ".format(username)
    plain_text_part = MIMEText(text_content, 'plain')
    # HTML content
    html_content = """\
    <html>
        <head></head>
        <body>
            <h1><b style="color:black;">Signup Successful!</b></h1>
            <p>Your username is: <b>{}</b></p>

        </body>
    </html>
    """.format(username, password)
    html_part = MIMEText(html_content, 'html')

    # Attach both plain text and HTML parts to the email
    message.attach(plain_text_part)
    message.attach(html_part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Confirmation email sent to {}.".format(email))
    except smtplib.SMTPException as e:
        print("Failed to send email: " + str(e))
    #     checking connection
    if db_connection.is_connected():
        print("Database connection successful!")
    # Create a cursor to execute SQL queries
        cursor = db_connection.cursor()
    # Insert user data into the database
        insert_query = """
        INSERT INTO users (username, password, name, gender, age, mobile, email, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_data = (username, password, name, gender, age, mobile, email, address)
        try:
            cursor.execute(insert_query, user_data)
            # Commit the changes and close the database connection
            db_connection.commit()
            cursor.close()
            #     db_connection.close()
            print("Signup successful!")
        except mysql.connector.Error as err:
            print("Error inserting data: {}".format(err))
            db_connection.rollback()

        # Close the database connection
        db_connection.close()
    else:
        print("Database connection failed.")


def login():
    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        # user_data = users.get(username)
        user_sender = "select password from users where username = %s"
        cursor = db_connection.cursor()
        cursor.execute(user_sender, (username,))
        sql_password = cursor.fetchone()

        cursor.close()

        if sql_password is None:
            print("Invalid Username")
        else:
            if sql_password[0] == password:
                print("Login successful!")
                return username
            else:
                print("Invalid username or password. Please try again.")


def main():
    print("Welcome to the Railway Ticket Booking System")

    while True:
        print("\nSelect an option:")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            usern = login()
            while True:
                print("1. Booking")
                print("2. Cancellation")
                print("3. Check PNR")
                print("4. Logout")
                user_input = int(input("Enter Your Choice: "))
                if user_input == 1:
                    trial = ticket_booking_process()
                    if db_connection.is_connected():
                        print("Database connection successful!")
                    # Create a cursor to execute SQL queries
                    cursor = db_connection.cursor()
                    passenger_info = [trial.passengers[i] if i < len(trial.passengers) else {} for i in range(6)]
                    tob_gen = datetime.now()
                    tob_gen = str(tob_gen)
                    tob = tob_gen.split('.')[0]
                    # Insert user data into the database
                    ticket_query = """
                        INSERT INTO tickets (   pnr, username, selected_quota, date_of_journey, 
                                                boarding , destination,email_id, total_fare,
                                                p1_name , p1_gender, p1_age, p1_phone, p1_address,
                                                p2_name , p2_gender, p2_age,
                                                p3_name , p3_gender, p3_age,
                                                p4_name , p4_gender, p4_age,
                                                p5_name , p5_gender, p5_age,
                                                p6_name , p6_gender, p6_age,
                                                p1_seat , p2_seat, p3_seat,
                                                p4_seat , p5_seat, p6_seat,
                                                p1_status, p2_status, p3_status,
                                                p4_status, p5_status, p6_status,tob

                                            )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s )  
                        """
                    user_data = (
                        trial.pnr, usern, trial.selected_quota, trial.date_str,
                        trial.boarding, trial.destination, trial.email_id, trial.total_fare,
                        passenger_info[0].get('name', 'Null'), passenger_info[0].get('gender', 'Null'),
                        passenger_info[0].get('age', 0), passenger_info[0].get('phone', 'Null'),
                        passenger_info[0].get('address', 'Null'),
                        passenger_info[1].get('name', 'Null'), passenger_info[1].get('gender', 'Null'),
                        passenger_info[1].get('age', 0),
                        passenger_info[2].get('name', 'Null'), passenger_info[2].get('gender', 'Null'),
                        passenger_info[2].get('age', 0),
                        passenger_info[3].get('name', 'Null'), passenger_info[3].get('gender', 'Null'),
                        passenger_info[3].get('age', 0),
                        passenger_info[4].get('name', 'Null'), passenger_info[4].get('gender', 'Null'),
                        passenger_info[4].get('age', 0),
                        passenger_info[5].get('name', 'Null'), passenger_info[5].get('gender', 'Null'),
                        passenger_info[5].get('age', 0),
                        passenger_info[0].get('seat', 'Null'), passenger_info[1].get('seat', 'Null'),
                        passenger_info[2].get('seat', 'Null'), passenger_info[3].get('seat', 'Null'),
                        passenger_info[4].get('seat', 'Null'), passenger_info[5].get('seat', 'Null'),
                        passenger_info[0].get('status', 'Null'), passenger_info[1].get('status', 'Null'),
                        passenger_info[2].get('status', 'Null'), passenger_info[3].get('status', 'Null'),
                        passenger_info[4].get('status', 'Null'), passenger_info[5].get('status', 'Null'),
                        tob
                    )

                    cursor.execute(ticket_query, user_data)
                    db_connection.commit()
                    cursor.close()
                elif user_input == 2:
                    print("...Cancellation...")
                    while True:
                        pnrc = input("Enter PNR No : ")
                        try:
                            if pnrc.isdigit() and len(pnrc) == 11:
                                pnr_obtain = '''SELECT date_of_journey, selected_quota, boarding, destination, 
                                p1_name, p1_seat, p1_status, p2_name, p2_seat, p2_status, p3_name, p3_seat, p3_status,
                                p4_name, p4_seat, p4_status, p5_name, p5_seat, p5_status, p6_name, p6_seat, p6_status, 
                                username , pnr
                                FROM tickets WHERE pnr=%s'''
                                cursor = db_connection.cursor()
                                cursor.execute(pnr_obtain, (pnrc,))
                                pnr_data = cursor.fetchall()
                                pnr_username = None
                                if pnr_data:
                                    pnr_username = pnr_data[0][22]
                                cursor.close()
                                if pnr_username is None:
                                    print("PNR not found")
                                    continue
                                elif usern == pnr_username:
                                    print(f"Date of Journey : {pnr_data[0][0]}")
                                    print(f"Quota : {pnr_data[0][1]}")
                                    print(f"Boarding : {pnr_data[0][2]}    Destination : {pnr_data[0][3]}")

                                    passenger_count = 0
                                    for i in range(4, 22, 3):
                                        passenger_name = pnr_data[0][i]
                                        if passenger_name != "Null":
                                            passenger_count += 1

                                            print(f"\n{passenger_count}", end=". ")
                                            print(f"Name: {passenger_name}", end=" | ")
                                            print(f"Seat: {pnr_data[0][i + 1]}", end=" | ")
                                            print(f"Status: {pnr_data[0][i + 2]}")
                                        #

                                    r = input("Enter the passenger no. to cancel the reservation : ")
                                    if r.isdigit():
                                            r = int(r)
                                            if 1 <= r <= passenger_count:
                                                can_num = 'p' + str(r) + '_status'
                                                
                                                can_check=3*(r+1)
                                                if pnr_data[0][can_check]!='CAN':
                                                    cursor = db_connection.cursor()
                                                    pnr_cancel = str(pnrc)
                                                    user_email = """SELECT email_id from tickets where pnr = %s """
                                                    cursor.execute(user_email, (pnr_cancel,))
                                                    user_email = cursor.fetchone()[0]
                                                    can_data = '''SELECT date_of_journey, selected_quota,
                                                         boarding, destination, 
                                                         p1_name, p1_seat, p1_status,
                                                         p2_name, p2_seat, p2_status,
                                                         p3_name, p3_seat, p3_status,
                                                         p4_name, p4_seat, p4_status,
                                                         p5_name, p5_seat, p5_status, 
                                                         p6_name, p6_seat, p6_status
                                                        FROM tickets WHERE pnr=%s'''


                                                    cancel_tic = f"""UPDATE tickets SET {can_num} ='CAN' WHERE pnr = %s"""
                                                    cursor.execute(cancel_tic, (pnr_cancel,))
                                                    db_connection.commit()
                                                    cursor.execute(can_data, (pnr_cancel,))
                                                    tic_data = cursor.fetchall()
                                                    cursor.close()
                                                    db_connection.close()

                                                    smtp_server = 'smtp.gmail.com'
                                                    smtp_port = 587
                                                    sender_email = 'reservation.cystum@gmail.com'
                                                    sender_password = 'dijeocfyweumpgam'
                                                    message = MIMEMultipart('alternative')
                                                    message['Subject'] = 'Ticket Cancellation'
                                                    message['From'] = sender_email
                                                    message['To'] = user_email
                                                    if not tic_data:
                                                        print("Some Error Occured\nPNR not Found")
                                                        continue
                                                    else:
                                                        email_can_content = f"<html><body>"
                                                        email_can_content += f"<p>Dear Passenger,</p>"
                                                        email_can_content += (f"<p>Your Ticket From <strong>"
                                                                              f"{tic_data[0][2]} "
                                                                              f"-> <strong>{tic_data[0][3]}"
                                                                              f"</strong> is Cancelled.</p>")

                                                        email_can_content += f"<p>Date of Journey: {tic_data[0][0]}</p>"
                                                        email_can_content += f"<p>Quota: {tic_data[0][1]}</p>"
                                                        email_can_content += f"<p><strong>Passenger Details:</strong></p>"
                                                        email_can_content += f"<table border='1' cellpadding='5'>"
                                                        email_can_content += f"<tr><th>SL No.</th><th>Name\
                                                                </th><th>Seat</th><th>Status</th></tr>"
                                                        passenger_count = 0
                                                        for i in range(4, len(tic_data[0]), 3):
                                                            passenger_name = tic_data[0][i]
                                                            if passenger_name != "Null":
                                                                passenger_count += 1
                                                                email_can_content += f"<tr>"
                                                                email_can_content += f"<td>{passenger_count}</td>"
                                                                email_can_content += f"<td>{passenger_name}</td>"
                                                                if tic_data[0][i+2] == 'CNF':
                                                                    email_can_content += f"<td>{tic_data[0][i + 1]}</td>"
                                                                    email_can_content += (f"<td style='color: green;'>"
                                                                                          f"{tic_data[0][i+2]}"
                                                                                          f"</td>")
                                                                else:
                                                                    email_can_content += f"<td>---</td>"
                                                                    email_can_content += (f"<td style='color: red;'>"
                                                                                          f"{tic_data[0][i+2]}"
                                                                                          f"</td>")
                                                                email_can_content += f"</tr>"

                                                        email_can_content += f"</table>"
                                                        email_can_content += f"<p><strong>Refund Information:</strong></p>"
                                                        email_can_content += f"<p>Your refund will be reverted to the \
                                                                same account in 4-5 working days.</p>"
                                                        email_can_content += f"</body></html>"
                                                    message.attach(MIMEText(email_can_content, 'html'))

                                                            # Connect to SMTP server and send email
                                                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                                                        server.starttls()
                                                        server.login(sender_email, sender_password)
                                                        server.sendmail(sender_email, user_email, message.as_string())
                                                    print("Ticket Cancelled successfully and email sent.")

                                                    break
                                                else:
                                                    print("The ticket for this passenger is already cancelled.")
                                                    break
                                                    
                                            else:
                                                print(f"Invalid Input {passenger_count} passenger/s for this PNR")
                                                continue
                                else:
                                    print("PNR does not belong to this user id.")
                                    continue
                            else:
                                print("PNR must be 11 digit number")
                                continue

                        except mysql.connector.Error as err:
                            print("Error:", err)
                    
                elif user_input == 3:
                    print("....Checking PNR....")
                    pnr_f = input("Enter PNR: ")
                    try:
                        if pnr_f.isdigit() and len(pnr_f) == 11:
                            pnr_details = '''SELECT date_of_journey, selected_quota, boarding, destination, 
                                p1_name, p1_seat, p1_status, p2_name, p2_seat, p2_status, p3_name, p3_seat, p3_status,
                                p4_name, p4_seat, p4_status, p5_name, p5_seat, p5_status, p6_name, p6_seat, p6_status
                                FROM tickets WHERE pnr=%s'''
                            cursor = db_connection.cursor()
                            cursor.execute(pnr_details, (pnr_f,))
                            pnr_data = cursor.fetchall()
                            cursor.close()
                            if not pnr_data:
                                print("PNR not found")
                                continue
                            else:
                                for row in pnr_data:
                                    print("+-----------------------------+")
                                    print("|Date of Journey:", row[0])
                                    print("+-----------------------------|")
                                    print("|Selected Quota:", row[1])
                                    print("+-----------------------------|")
                                    print("|Boarding Point:", row[2])
                                    print("+-----------------------------|")
                                    print("|Destination:", row[3])
                                    print("+-----------------------------+")

                                    passenger_count = 0

                                    for i in range(4, len(row), 3):
                                        passenger_name = row[i]
                                        if passenger_name != "Null":
                                            passenger_count += 1

                                            print(f"\nPassenger {passenger_count}:")
                                            print("+-----------------------------+")
                                            print("|  Name:", passenger_name)
                                            print("+-----------------------------|")
                                            print("|  Seat:", row[i + 1])
                                            print("+-----------------------------|")
                                            print("|  Status:", row[i + 2])
                                            print("+-----------------------------+")
                        else:
                            print("PNR must be 11 digit number")
                            continue
                    except mysql.connector.Error as err:
                        print("Error:", err)

                elif user_input == 4:
                    print("Logout Successfully")
                    break
                else:
                    continue
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


def ticket_booking_process():
    booking = TicketBooking()
    booking.display_quota_options()
    booking.book_tickets()
    booking.print_tickets()
    return booking


if __name__ == "__main__":
    main()
