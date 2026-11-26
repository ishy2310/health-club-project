from models import Bill, ClassSession, GroupFitnessClass, PTSession, Payment, Room
from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker


class AdminController:
    # Class management
        # Define new classes
    def createNewFitnessClass(self, session, class_name, class_description, class_capacity):
        new_class = GroupFitnessClass(name = class_name, description = class_description,capacity = class_capacity,)
        session.add(new_class)

    def createNewClassSession(self, session, fitness_class_id, class_capacity):
        new_class_session = ClassSession(class_id = fitness_class_id, capacity= class_capacity,)
        session.add(new_class_session)
        # trainer_id = class_trainer_id, room_id= class_room_id,

        # Assign Trainers/Rooms/Time to classes + Update Schedules
    def assignTrainer(self, session, class_session_id, class_trainer_id):
        session.execute(update(ClassSession).where(ClassSession.session_id == class_session_id).values(trainer_id=class_trainer_id))

    def assignClassSessionRoom(self, session, class_session_id, class_room_id):
        session.execute(
            update(ClassSession).where(ClassSession.session_id == class_session_id).values(room_id=class_room_id))

            # Room Booking: Assign rooms for session OR CLASSES
    def assignPTSessionRoom(self, session, PT_session_id, class_room_id):
        session.execute(update(PTSession).where(PTSession.pt_id == PT_session_id).values(room_id=class_room_id))

    def assignTime(self, session, class_session_id,class_date, class_start_time, class_end_time):
        session.execute(update(ClassSession).where(ClassSession.session_id == class_session_id).values(date=class_date, start_time=class_start_time, end_time=class_end_time))
    
    # Billing and Payment

        # Generate bills
    def createBill(self, session, bill_total, bill_date):
        new_bill = Bill(total = bill_total, date=bill_date)
        session.add(new_bill)
        #member_id = bill_member_id,

        # Add line items

        # record payments
    def createPayment(self, session, payment_bill_id, payment_method, payment_amount, payment_date):
        new_bill = Payment(member_id = bill_member_id, total = bill_total, date=bill_date)
        session.add(new_bill)

    # Simulate status update
    def updateBillStatus(self, session, payment_bill_id, bill_status):
        session.execute(update(Bill) .where(Bill.bill_id == payment_bill_id).values(status=bill_status))
    
    # Print out information
        # Print out all Fitness Classes
    def printAllFitnessClasses(self, session):
        fitness_classes = session.scalars(select(GroupFitnessClass)).all()
        print(f"\n=== Group Fitness Classes ({len(fitness_classes)}) ===")
        if not fitness_classes:
            print("(none)")
        for fc in fitness_classes:
            print(f"Class ID:    {fc.class_id}\nName:        {fc.name}\nDescription: {fc.description}\nCapacity:    {fc.capacity}\n")
    
        # Print out all class sessions
    def printAllClassSessions(self,session):
        class_sessions = session.scalars(select(ClassSession)).all()
        print(f"\n=== Class Sessions ({len(class_sessions)}) ===")
        if not class_sessions:
            print("(none)")
        for cs in class_sessions:
            print(f"Session ID: {cs.session_id}\nClass ID:   {cs.class_id}\nTrainer ID: {cs.trainer_id}\nRoom ID:    {cs.room_id}\nDate:       {cs.date}\nStart:      {cs.start_time}\nEnd:        {cs.end_time}\nCapacity:   {cs.capacity}\nStatus:     {cs.class_session_status.value}\n")

        #Print out all ptsessions
    def printAllPTSessions(self, session):
        pt_sessions = session.scalars(select(PTSession)).all()
        print(f"\n=== PT Sessions ({len(pt_sessions)}) ===")
        if not pt_sessions:
            print("(none)")
        for pt in pt_sessions:
            print(f"  PT ID:      {pt.pt_id}\nMember ID:  {pt.member_id}\nTrainer ID: {pt.trainer_id}\nRoom ID:    {pt.room_id}\nDate:       {pt.date}\nStart:      {pt.start_time}\nEnd:        {pt.end_time}\nStatus:     {pt.status.value}\n")
        
        # Print out all  bills
    def printAllBills(self,session):
        bills = session.scalars(select(Bill)).all()
        print(f"\n=== Bills ({len(bills)}) ===")
        if not bills:
            print("  (none)")
        for bill in bills:
            # Prints every column, since I haven't seen your Bill model
            for col in bill.__table__.columns:
                print(f"  {col.name}: {getattr(bill, col.name)}")
            print()

        #Print out payments 
    def printAllPayments(self,session):
        payments = session.scalars(select(Payment)).all()
        print(f"\n=== Payments ({len(payments)}) ===")
        if not payments:
            print("  (none)")
        for payment in payments:
            # Prints every column, since I haven't seen your Payment model
            for col in payment.__table__.columns:
                print(f"  {col.name}: {getattr(payment, col.name)}")
            print()

        # print out specific bills    
    def printBill(self,session, bill_id):
        bill = session.get(Bill, bill_id)
        if bill is None:
            print(f"\nBill with id {bill_id} not found.")
            return None
        print(f"\n=== Bill {bill_id} ===")
        for col in bill.__table__.columns:
            print(f"  {col.name}: {getattr(bill, col.name)}")
        return bill

        # print out specific payments
    def printPayment(self,session, payment_id):
        payment = session.get(Payment, payment_id)
        if payment is None:
            print(f"\nPayment with id {payment_id} not found.")
            return None
        print(f"\n=== Payment {payment_id} ===")
        for col in payment.__table__.columns:
            print(f"  {col.name}: {getattr(payment, col.name)}")
        return payment

        # print out specific class sessions
    def printClassSession(self,session, class_session_id):
        cs = session.get(ClassSession, class_session_id)
        if cs is None:
            print(f"\nClass session with id {class_session_id} not found.")
            return None
        print(f"\n=== Class Session {class_session_id} ===")
        print(f"Session ID: {cs.session_id}\nClass ID:   {cs.class_id}\nTrainer ID: {cs.trainer_id}\nRoom ID:    {cs.room_id}\nDate:       {cs.date}\nStart:      {cs.start_time}\nEnd:        {cs.end_time}\nCapacity:   {cs.capacity}\nStatus:     {cs.class_session_status.value}")
        return cs

        # print out specific fitness classes
    def printFitnessClass(self,session, fitness_class_id):
        fc = session.get(GroupFitnessClass, fitness_class_id)
        if fc is None:
            print(f"\nFitness class with id {fitness_class_id} not found.")
            return None
        print(f"\n=== Group Fitness Class {fitness_class_id} ===")
        print(f"  Class ID:    {fc.class_id}\nName:        {fc.name}\nDescription: {fc.description}\nCapacity:    {fc.capacity}")
        return fc

        # print out specific ptsessions
    def printPTSession(self,session, pt_session_id):
        pt = session.get(PTSession, pt_session_id)
        if pt is None:
            print(f"\nPT session with id {pt_session_id} not found.")
            return None

        print(f"\n=== PT Session {pt_session_id} ===")
        print(f"  PT ID:      {pt.pt_id}\nMember ID:  {pt.member_id}\nTrainer ID: {pt.trainer_id}\nRoom ID:    {pt.room_id}\nDate:       {pt.date}\nStart:      {pt.start_time}\nEnd:        {pt.end_time}\nStatus:     {pt.status.value}")
       
        return pt

    # Helper functions
    def checkInput(self, valid_inputs):
        while True:
            try:
                choice = print(int(input(": ")))
                if choice not in valid_inputs:
                    print("Please enter a valid option.")
                    continue;
                else:
                    return choice;
            except ValueError:
                print("Please enter a valid option.")

    def checkDbInput(self, session, type):
        while True:
            try:
                choice = print(int(input(": ")))
                selected = session.get(type, choice)
                if selected is None:
                    print("Please enter a valid option.")
                    continue;
                else:
                    return choice;
            except ValueError:
                print("Please enter a valid option.")

    
    def isRoomAssigned(self, session, room_id, check_date, start_time, end_time):
        for model in (PTSession, ClassSession):
            conflict = select(model).where(
                model.room_id == room_id,
                model.date == check_date,
                model.start_time < end_time,
                model.end_time > start_time,
            )
            if session.scalars(conflict.limit(1)).first():
                return True
        return False

    def getAvailableRooms(self,session, class_session_id=None, pt_session_id=None):
        if class_session_id is not None:
            target = session.get(ClassSession, class_session_id)
        else:
            target = session.get(PTSession, pt_session_id)

        all_rooms = session.scalars(select(Room).order_by(Room.room_id)).all()
        return [
            room for room in all_rooms
            if not self.isRoomAssigned(session, room.room_id, target.date, target.start_time, target.end_time)
        ]

    # Menus
        # Main Menu
    def adminMenu(session):
        valid_inputs = {1, 2, 3, 4, 5}

        print(f"\n=== Admin Menu ===")
        print(f"\n1. Room Booking\n2. Equipment Maintenance:\n3. Class Management:\n4. Billing & Payment:\n5. Return to Homepage")

        choice = self.checkInput(valid_inputs)
        
        match choice:
            case 1:
                roomBooking(session)

    # Room Booking

    def roomBooking(session):
        valid_inputs = {1, 2, 3}


        print(f"\n=== Room Booking Menu ===")
        print(f"\n1.PTSession \n2. Group Fitness Class\n3. Return to Admin Menu")

        choice = self.checkInput(valid_inputs)

        match choice:
            case 1:
                print(f"\n=== Which PT Session would you like to assign a room to? ===")
                self.printAllPTSessions(session)

                selected = self.checkDbInput(session, PTSession)

                print(f"\n=== Which Room would you like to assign? ===")                    
                availableRooms = self.getAvailableRooms(session, pt_session_id = selected)

                if not availableRooms:
                    print("No rooms are available at that time for that session")
                    return None

                for room in availableRooms:
                    print(f"  {room.room_id}: {room.name}")
                
                valid_inputs = [room.room_id for room in rooms]

                choice = self.checkInput(valid_inputs)

                self.assignPTSessionRoom(session, selected, choice)
            
            case _:
                print("no choice chosen")






