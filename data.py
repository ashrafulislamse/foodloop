# FoodLoop sample data for the demo
from models import Donation, Recipient

# the three organisations used in the demonstration
def get_sample_recipients():
    recipients = []
    recipients.append(Recipient("Hope Food Bank KL", "food bank", 200, "any"))
    recipients.append(Recipient("Rumah Penyayang Ampang", "orphanage", 60, "cooked"))
    recipients.append(Recipient("Pertubuhan Amal Seri Kembangan", "welfare home", 100, "any"))
    return recipients

# five donations, one already expired so the safety check is visible
def get_sample_donations():
    donations = []
    donations.append(Donation("Cafe Ria", "Vegetable rice", "cooked", 40, 1))
    donations.append(Donation("Baker House KL", "Fresh bread and buns", "packed", 80, 3))
    donations.append(Donation("Pasar Taman Segar", "Fresh vegetables", "raw", 30, 2))
    donations.append(Donation("Grandza Catering", "Fried chicken packs", "cooked", 50, 0))
    donations.append(Donation("Mydin Meru", "Canned food packs", "packed", 120, 10))
    return donations
