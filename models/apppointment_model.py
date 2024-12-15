class Appointment:
	def __init__(self, apt_type, apt_category, apt_date, apt_session, apt_number, customer_phone, customer_email, status, description, rating, apt_id):
		self.apt_id = apt_id
		self.apt_type = apt_type
		self.apt_category = apt_category
		self.apt_date = apt_date
		self.apt_session = apt_session
		self.apt_number = apt_number
		self.customer_phone = customer_phone
		self.customer_email = customer_email
		self.status = status
		self.description = description
		self.rating = rating

	def to_qr_data(self):
		if self.apt_type != 'On-demand':
			the_string = f"""
Type : {self.apt_type}
Date : {self.apt_date}
Session : {self.apt_session}
Queue number : {self.apt_number}
Phone number : {self.customer_phone}
Email : {self.customer_email}
			"""
		else:
			the_string = f"""
Type : {self.apt_type}
Category : {self.apt_category}
Date : {self.apt_date}
Session : {self.apt_session}
Queue number : {self.apt_number}
Phone number : {self.customer_phone}
Email : {self.customer_email}
			"""
		return the_string