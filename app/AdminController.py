from models import Bill, ClassSession
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker


class AdminController:

    def __init__(engine):
        self.session =  sessionmaker(bind=engine)

    # Class management
        # Define new classes
    def createNewFitnessClass(class_name, class_description, class_date, class_capacity):
        with Session() as session:
            new_class = ClassSession(name = class_name, description = class_description, date=class_date ,capacity= class_capacity)
            session.add(new_class)
            session.commit()

    def createNewClassSession(fitness_class_id, class_capacity):
        with Session() as session:
            new_class_session = ClassSession(class_id = fitness_class_id, capacity= class_capacity)
            session.add(new_class_session)
            session.commit()

        # Assign Trainers/Rooms/Time to classes + Update Schedules
    def assignTrainer(class_session_id, class_trainer_id):
        update(class_session_table).where(class_session_table.c.session_id == class_session_id).values(trainer_id=class_trainer_id)

    def assignClassSessionRoom(class_session_id, class_room_id):
        update(class_session_table).where(class_session_table.c.session_id == class_session_id).values(room_id=class_room_id)

            # Room Booking: Assign rooms for session OR CLASSES
    def assignPTSessionRoom(PT_session_id, class_room_id):
        update(PT_session_table).where(PT_session_table.c.pt_id == PT_session_id).values(room_id=class_room_id)


    def assignTime(class_session_id, class_start_time, class_end_time):
        update(class_session_table).where(class_session_table.c.session_id == class_session_id).values(start_time=class_start_time, end_time = class_end_time)

    
    # Billing and Payment

        # Generate bills
    def createBill(bill_member_id, bill_total, bill_date):
        with Session() as session:
            new_bill = Bill(member_id = bill_member_id, total = bill_total, date=bill_date)
            session.add(new_bill)
            session.commit()

        # Add line items

        # record payments
    def createPayments(payment_bill_id, payment_method, payment_amount, payment_date):
        with Session() as session:
            new_bill = Bill(member_id = bill_member_id, total = bill_total, date=bill_date)
            session.add(new_bill)
            session.commit()

    # Simulate status update
    def updateBillStatus(payment_bill_id, bill_status):
        update(bill_table).where(bill_table.c.member_id == payment_bill_id).values(status = bill_status)
