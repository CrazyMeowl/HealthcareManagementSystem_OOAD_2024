class User:
    def __init__(self, full_name, phone_number, email, gender, date_of_birth, ssn, password, height=None, weight=None, blood_type=None, role='user'):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.ssn = ssn 
        self.password = password
        self.height = height
        self.weight = weight
        self.blood_type = blood_type
        self.role = role
    
