from models import Bill, ClassSession, GroupFitnessClass, PTSession, Payment, Room, Equipment
from models.Payment import Status as PaymentStatus, Method as PaymentMethod
from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class AdminController:

    def __init__(engine):
        self.Session = sessionmaker(bind=engine)

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

    def assignTime(class_session_id, class_start_time, class_end_time):
        update(class_session_table).where(class_session_table.c.session_id == class_session_id).values(start_time=class_start_time, end_time = class_end_time)

    
    # Billing and Payment

        # Generate bills
    def createBill(self, session, bill_total, bill_date):
        new_bill = Bill(total = bill_total, date=bill_date)
        session.add(new_bill)

        # Add line items

        # record payments
    def createPayment(self, session, payment_bill_id, payment_method, payment_amount, payment_date):
        new_bill = Payment(member_id = bill_member_id, total = bill_total, date=bill_date)
        session.add(new_bill)

    # Simulate status update
    def updateBillStatus(self, session, payment_bill_id, bill_status):
        session.execute(update(Bill) .where(Bill.bill_id == payment_bill_id).values(status=bill_status))
    
    # Equipement Maintenance
    def createMaintenanceLog(self, session, equipment_id, issue_description):
        new_log = MaintenanceLog(equipment_id=equipment_id, issue_description=issue_description)
        session.add(new_log)

    def assignEquipmentRoom(self, session, equipment_id, room_id):
        session.execute(
            update(Equipment)
            .where(Equipment.equipment_id == equipment_id)
            .values(room_id=room_id)
        )

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

    def printMaintenanceLogsByStatus(self, session, status, title):
        logs = session.scalars(select(MaintenanceLog).where(MaintenanceLog.status == status).order_by(MaintenanceLog.reported_date)).all()

        print(f"\n=== {title} ({len(logs)}) ===")
        if not logs:
            print("(none)")
        for log in logs:
            eq = log.equipment
            print(
                f"Log ID:      {log.log_id}\n"
                f"Equipment:   {eq.equipment_id} ({getattr(eq, 'name', 'unnamed')})\n"
                f"Room ID:     {eq.room_id}\n"
                f"Issue:       {log.issue_description}\n"
                f"Reported:    {log.reported_date}\n"
                f"Status:      {log.status}\n"
            )

    def printAllBills(self, session):
        bills = session.scalars(select(Bill).order_by(Bill.bill_id)).all()
        print(f"\n=== Bills ({len(bills)}) ===")
        if not bills:
            print("(none)")
        for bill in bills:
            print(
                f"Bill ID:   {bill.bill_id}\n"
                f"Member ID: {bill.member_id}\n"
                f"Date:      {bill.date}\n"
                f"Total:     ${bill.total:.2f}\n"
                f"Status:    {bill.status.value}"
            )
            if bill.payments:
                paid = sum(p.amount for p in bill.payments if p.status.value == "completed")
                print(f"Payments:  {len(bill.payments)} (${paid:.2f} completed)")
            print()

    # Helper functions
    def checkInput(self, valid_inputs):
        """Prompt until the user enters an integer found in valid_inputs."""
        while True:
            try:
                choice = int(input(": "))
            except ValueError:
                print("Please enter a valid option.")
                continue
            if choice not in valid_inputs:
                print("Please enter a valid option.")
                continue
            return choice

    def checkDbInput(self, session, model):
        """Prompt until the user enters an id that exists in the given model's table."""
        while True:
            try:
                choice = int(input(": "))
            except ValueError:
                print("Please enter a valid option.")
                continue
            if session.get(model, choice) is None:
                print("Please enter a valid option.")
                continue
            return choice

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

    def getAvailableRooms(self, session, class_session_id=None, pt_session_id=None):
        if class_session_id is not None:
            target = session.get(ClassSession, class_session_id)
        else:
            target = session.get(PTSession, pt_session_id)

        all_rooms = session.scalars(select(Room).order_by(Room.room_id)).all()
        return [
            room for room in all_rooms
            if not self.isRoomAssigned(
                session, room.room_id, target.date, target.start_time, target.end_time
            )
        ]


    def printMaintenanceLogsByStatus(self, session, status, title):
        logs = session.scalars(
            select(MaintenanceLog)
            .where(MaintenanceLog.status == status)
            .order_by(MaintenanceLog.reported_date)
        ).all()

        print(f"\n=== {title} ({len(logs)}) ===")
        if not logs:
            print("(none)")
        for log in logs:
            eq = log.equipment
            print(
                f"Log ID:      {log.log_id}\n"
                f"Equipment:   {eq.equipment_id} ({getattr(eq, 'name', 'unnamed')})\n"
                f"Room ID:     {eq.room_id}\n"
                f"Issue:       {log.issue_description}\n"
                f"Reported:    {log.reported_date}\n"
                f"Status:      {log.status}\n"
            )

    def printAllEquipment(self, session):
        equipment = session.scalars(select(Equipment).order_by(Equipment.equipment_id)).all()
        print(f"\n=== Equipment ({len(equipment)}) ===")
        if not equipment:
            print("(none)")
        for eq in equipment:
            print(f"  {eq.equipment_id}: {getattr(eq, 'name', 'unnamed')} (Room ID: {eq.room_id})")

    # Menus
        # Main Menu
    def adminMenu(session):
        valid_inputs = {1, 2, 3, 4, 5}

        while True:
            print("\n=== Admin Menu ===")
            print("\n1. Room Booking\n2. Equipment Maintenance\n3. Class Management\n4. Billing & Payment\n5. Return to Homepage")

            choice = self.checkInput(valid_inputs)

            match choice:
                case 1:
                    self.roomBooking(session)
                case 2:
                    self.billingPayment(session)
                case 3:
                    self.classManagement(session)
                case 4:
                    self.equipementManagement(session)
                case 5:
                    return True

    # Room Booking
    def roomBooking(session):
        valid_inputs = {1, 2, 3}

        print("\n=== Room Booking Menu ===")
        print("\n1. PT Session\n2. Group Fitness Class\n3. Return to Admin Menu")

        choice = self.checkInput(valid_inputs)

        match choice:
            case 1:
                print("\n=== Which PT Session would you like to assign a room to? ===")
                self.printAllPTSessions(session)
                selected = self.checkDbInput(session, PTSession)

                available_rooms = self.getAvailableRooms(session, pt_session_id=selected)
                if not available_rooms:
                    print("No rooms are available at that time for that session.")
                    return None

                print("\n=== Which Room would you like to assign? ===")
                for room in available_rooms:
                    print(f"  {room.room_id}: {room.name}")

                room_choice = self.checkInput({room.room_id for room in available_rooms})

                self.assignPTSessionRoom(session, selected, room_choice)
                session.commit()
                print("\nRoom assigned.")
                return True

            case 2:
                print("\n=== Which Group Fitness Session would you like to assign a room to? ===")
                self.printAllClassSessions(session)
                selected = self.checkDbInput(session, ClassSession)

                available_rooms = self.getAvailableRooms(session, class_session_id=selected)
                if not available_rooms:
                    print("No rooms are available at that time for that session.")
                    return None

                print("\n=== Which Room would you like to assign? ===")
                for room in available_rooms:
                    print(f"  {room.room_id}: {room.name}")

                room_choice = self.checkInput({room.room_id for room in available_rooms})

                self.assignClassSessionRoom(session, selected, room_choice)
                session.commit()
                print("\nRoom assigned.")
                return True

            case 3:
                print("\n=== Returning to Admin Menu ===\n")
                return True


    # Class Management
    def classManagement(session):
        valid_inputs = {1,2,3,4}

        while True:
            print("\n=== Class Management Menu ===")
            print("\n1. Create a new fitness class\n2. Create a new class session\n3. Update class session\n4. Return to Admin Menu")

            choice = self.checkInput(valid_inputs)

            match choice:
                case 1:
                    print("\n=== New Fitness Class ===")
                    try:
                        class_name = input("Class name: ").strip()
                        class_description = input("Class description: ").strip()
                        class_capacity = int(input("Class capacity: "))
                    except ValueError:
                        print("\nInvalid input: capacity must be a number.")
                        continue

                    if not class_name or class_capacity <= 0:
                        print("\nName is required and capacity must be positive.")
                        continue

                    self.createNewFitnessClass(session, class_name, class_description, class_capacity)
                    session.commit()
                    print("\nFitness class created.")

                case 2:
                    print("\n=== New Class Session ===")
                    self.printAllFitnessClasses(session)
                    print("Which class is this session for?")
                    fitness_class_id = self.checkDbInput(session, GroupFitnessClass)

                    try:
                        class_capacity = int(input("Session capacity: "))
                    except ValueError:
                        print("\nInvalid input: capacity must be a number.")
                        continue

                    self.createNewClassSession(session, fitness_class_id, class_capacity)
                    session.commit()
                    print("\nClass session created.")

                case 3:
                    print("\n=== Update Class Session ===")
                    self.printAllClassSessions(session)
                    print("Which session would you like to update?")
                    session_id = self.checkDbInput(session, ClassSession)

                    print("\n1. Assign trainer\n2. Set date and time\n3. Back")
                    sub = self.checkInput({1, 2, 3})

                    if sub == 1:
                        try:
                            trainer_id = int(input("Trainer ID: "))
                        except ValueError:
                            print("\nInvalid input.")
                            continue
                        self.assignTrainer(session, session_id, trainer_id)
                        session.commit()
                        print("\nTrainer assigned.")

                    elif sub == 2:
                        try:
                            class_date = datetime.strptime(input("Date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                            start = datetime.strptime(input("Start time (HH:MM): "), "%H:%M").time()
                            end = datetime.strptime(input("End time (HH:MM): "), "%H:%M").time()
                        except ValueError:
                            print("\nInvalid date/time format.")
                            continue
                        if end <= start:
                            print("\nEnd time must be after start time.")
                            continue
                        self.assignTime(session, session_id, class_date, start, end)
                        session.commit()
                        print("\nTime updated.")

                case 4:
                    print("\n=== Returning to Admin Menu ===\n")
                    return True
    
    def equipmentMaintenance(session):
        valid_inputs = {1,2,3,4}

        while True:
            print("\n=== Equipment Maintenance Menu ===")
            print("\n1. Create Maintenance Log\n2. View all Equipement By Status\n3. Assign Equipement to Room\n4. Return to Admin Menu")

            choice = self.checkInput(valid_inputs)

            match choice:
                case 1:
                    print("\n=== New Maintenance Log ===")
                    self.printAllEquipment(session)
                    equipment_id = self.checkDbInput(session, Equipment)

                    issue = input("Describe the issue: ").strip()
                    if not issue:
                        print("\nAn issue description is required.")
                        continue

                    self.createMaintenanceLog(session, equipment_id, issue)
                    session.commit()
                    print("\nMaintenance log created.")

                case 2:
                    print("\n=== Open Logs ===")

                    self.printMaintenanceLogsByStatus(session, "OPEN", "Broken Equipment")

                    rint("\n=== Equipment Under Repair ===")

                    self.printMaintenanceLogsByStatus(session, "IN_PROGRESS", "Equipment Under Repair")

                case 3:
                    print("\n=== Which equipment would you like to move? ===")
                    self.printAllEquipment(session)
                    equipment_id = self.checkDbInput(session, Equipment)

                    rooms = session.scalars(select(Room).order_by(Room.room_id)).all()
                    if not rooms:
                        print("\nNo rooms exist yet.")
                        continue

                    print("\n=== Which room would you like to assign it to? ===")
                    for room in rooms:
                        print(f"  {room.room_id}: {room.name} ({room.type.value})")

                    room_id = self.checkInput({room.room_id for room in rooms})

                    self.assignEquipmentRoom(session, equipment_id, room_id)
                    session.commit()
                    print("\nEquipment assigned to room.")

                case 4:
                        print("\n=== Returning to Admin Menu ===\n")
                        return True

    def billingPayment(session):
        valid_inputs = {1,2,3,4,5}

        while True:
            print("\n=== Billing and Payment Menu ===")
            print("\n1. Create bills\n2. Create payment\n3. Update Payment Status\n4. Update Bill Status\n5. Return to Admin Menu")

            choice = self.checkInput(valid_inputs)

            match choice:
                case 1:
                    print("\n=== New Bill ===")

                    try:
                        bill_total = int(input("Bill Total "))
                        bill_date = datetime.strptime(input("Date (YYYY-MM-DD): "), "%Y-%m-%d").date()

                    except ValueError:
                        print("\nInvalid input.")
                        continue

                    self.createBill(session, bill_total, bill_date)
                    session.commit()

                case 2:
                    print("\n=== New Payment ===")

                    try:
                        self.printAllBills(session)
                        payment_bill_id = self.checkDbInput(session, Bill)
                        payment_amount = int(input("Payment Amount "))

                        print("\nPayment method:")
                        payment_method = self.chooseEnum(PaymentMethod)
                        payment_date = datetime.strptime(input("Date (YYYY-MM-DD): "), "%Y-%m-%d").date()

                        amount = int(input("Payment Amount "))
                        if amount is None:
                            continue


                    except ValueError:
                        print("\nInvalid input.")
                        continue

                    self.createPayment(session, payment_bill_id, payment_method, payment_amount, payment_date)
                    session.commit()

                case 3:
                    print("\n=== Update Payment Status ===")
                    if not self.hasRows(session, Payment):
                        print("\nNo payments exist yet.")
                        continue

                    self.printAllPayments(session)
                    print("Which payment would you like to update?")
                    payment_id = self.checkDbInput(session, Payment)

                    print("\nNew status:")
                    new_status = self.chooseEnum(PaymentStatus)

                    self.updatePaymentStatus(session, payment_id, new_status)
                    session.commit()
                    print("\nPayment status updated.")

                case 4:
                    print("\n=== Update Bill Status ===")
                    if not self.hasRows(session, Bill):
                        print("\nNo bills exist yet.")
                        continue

                    self.printAllBills(session)
                    print("Which bill would you like to update?")
                    bill_id = self.checkDbInput(session, Bill)

                    print("\nNew status:")
                    new_status = self.chooseEnum(BillStatus)

                    self.updateBillStatus(session, bill_id, new_status)
                    session.commit()
                    print("\nBill status updated.")

                case 5:
                        print("\n=== Returning to Admin Menu ===\n")
                        return True