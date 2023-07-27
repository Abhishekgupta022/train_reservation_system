from random import randint
from datetime import datetime, timedelta
import calendar
import smtplib
from email.mime.text import MIMEText
import getpass
from email_validator import validate_email, EmailNotValidError
import csv



file_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\vs code C\\Python\\station_name_code.csv"


class TicketBooking:
    def select_boarding_details(self):
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
        self.seat_details = self.generate_seat_details()
        self.pnr = self.generate_pnr()

    def display_quota_options(self):
        for ind, quota in enumerate(self.quota_options):
            print('{}: {}'.format(ind + 1, quota))

    def select_quota(self):
        choice = input("Enter the corresponding number for the quota: ")
        choice = int(choice)
        if 1 <= choice <= len(self.quota_options):
            selected_quota = self.quota_options[choice - 1]
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
                day = selected_date.weekday()
                if today <= selected_date <= future_limit:
                    print("You selected:", selected_date)
                    return selected_date , calendar.day_name[day]
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
        passenger_count = int(input("Enter the number of passengers: "))
        selected_quota = self.select_quota()
        selected_date,day = self.select_date()
        self.passengers = []

        boarding, destination = self.select_boarding_details()
        for i in range(passenger_count):
            passenger = self.get_passenger_info(i + 1, selected_quota)
            self.passengers.append(passenger)

        smtp_username = getpass.getpass("SMTP Username: ")
        smtp_password = getpass.getpass("SMTP Password: ")
        email_id = input("Enter the Email ID for receiving the ticket details: ")
        self.send_email(self.passengers, boarding, destination,selected_date,day, email_id, smtp_username, smtp_password)

    def get_passenger_info(self, i, selected_quota):
        name = input("Enter the Name of Passenger {}: ".format(i))
        print("Select passenger {} Gender".format(i))
        gender_options = ['Male', 'Female', 'Trans']
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
            age = input('Enter the age of passenger {}: '.format(i))
            if age.isdigit():
                age = int(age)
                break
            else:
                print("Invalid input! Enter a numeric age.\n")

        valid_mob = False
        while not valid_mob:
            mob = input("Enter the Phone no. of passenger {}: ".format(i))
            if len(mob) == 10 and mob.isdigit() and mob[0] != '0':
                valid_mob = True
            else:
                print(
                    "Invalid phone number! Enter the phone number without the country code and make sure it does not start with 0.\n")

        address = input("Enter the passenger {} address: ".format(i))

        quota = self.quota_options.index(selected_quota)
        seat_details = self.seat_details[self.quota_options[quota]]
        coach_number = randint(1, seat_details['total_coaches'])
        seat_number = i
        seat = "{}{}:{}".format(seat_details['coach'], coach_number, seat_number)

        if i == 1:
            fare = self.calculate_fare(selected_quota)
        else:
            fare = self.passengers[0]['fare']

        passenger_info = {
            'name': name,
            'gender': selected_gender,
            'age': age,
            'phone': mob,
            'address': address,
            'seat': seat,
            'pnr': self.pnr,
            'fare': fare
        }
        return passenger_info

    @staticmethod
    def generate_pnr():
        pnr = randint(10 ** 10, (10 ** 11) - 1)
        return pnr

    def calculate_total_fare(self):
        total_fare = sum(passenger['fare'] for passenger in self.passengers)
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
            print("----*----*----*----*----*----*----*----")

        total_fare = self.calculate_total_fare()
        print("Total Fare: Rs.", total_fare)

    def send_email(self, passengers, boarding, destination, selected_date,day,email_id,smtp_username, smtp_password):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'abhishek.rouniyar1@gmail.com'

        message = MIMEText('','html')
        message['Subject'] = 'Ticket Booking Confirmation'
        message['From'] = sender_email
        email_content = "<html><body>"
        email_content += "<p>Dear Passenger, your ticket details for the journey from <b>{}</b> to <b>{}</b> :</p>".format(boarding, destination)
        email_content += "<p>Date Of Journey: <b>{} ({})</b></p>".format(selected_date, day)
        email_content += "<br>"

        for passenger in passengers:
            email_content += "<hr>"
            email_content += "<p>Passenger Name: <b>{}</b></p>".format(passenger['name'])
            email_content += "<p>Gender: <b>{}</b></p>".format(passenger['gender'])
            email_content += "<p>Age: <b>{}</b></p>".format(str(passenger['age']))
            email_content += "<p>Phone Number: <b>{}</b></p>".format(str(passenger['phone']))
            email_content += "<p>Address: <b>{}</b></p>".format(str(passenger['address']))
            email_content += "<p>Seat: <b>{}</b></p>".format(str(passenger['seat']))
            email_content += "<p>PNR: <b>{}</b></p>".format(str(passenger['pnr']))
            email_content += "<p>Fare: <b>{}</b></p>".format(str(passenger['fare']))
            email_content += "<hr>"

        total_fare = self.calculate_total_fare()
        email_content += "<p>Total Fare: Rs. <b>{}</b></p>".format(total_fare)
        email_content += "</body></html>"

        message.set_payload(email_content)
        message['To'] = email_id

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)


def ticket_booking_process():
    booking = TicketBooking()
    booking.display_quota_options()
    booking.book_tickets()
    booking.print_tickets()

# iiwdvtilcxknsntp
# pkeqoyyklaxxvhjk
# rujtjuncoeetrggx
# iiwdvtilcxknsntp
ticket_booking_process()
