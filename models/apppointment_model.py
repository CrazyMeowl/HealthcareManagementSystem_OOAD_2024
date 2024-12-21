class Appointment:
	def __init__(self, apt_type, apt_category, apt_date, apt_session, apt_number, apt_description, customer_phone, customer_email, status,rating, apt_id):
		self.apt_id = apt_id
		self.apt_type = apt_type
		self.apt_category = apt_category
		self.apt_date = apt_date
		self.apt_session = apt_session
		self.apt_number = apt_number
		self.apt_description = apt_description
		self.customer_phone = customer_phone
		self.customer_email = customer_email
		self.status = status
		self.rating = rating

