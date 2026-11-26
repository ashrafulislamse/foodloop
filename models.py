# FoodLoop data classes
# Donation holds one food donation record

class Donation:
    def __init__(self, donor, food_name, category, servings, expiry_days):
        self.donor = donor
        self.food_name = food_name
        self.category = category
        self.servings = servings
        self.expiry_days = expiry_days

    # a batch with zero or fewer days left cannot be used
    def is_expired(self):
        return self.expiry_days <= 0

    # the urgency shown next to each batch
    def urgency_label(self):
        if self.is_expired():
            return "EXPIRED - DO NOT USE"
        elif self.expiry_days <= 2:
            return "URGENT"
        elif self.expiry_days <= 7:
            return "SOON"
        else:
            return "FRESH"

# Recipient holds one community organisation that can receive food
# received_servings tracks stock already allocated to this recipient

class Recipient:
    def __init__(self, name, org_type, capacity_servings, food_category):
        self.name = name
        self.org_type = org_type
        self.capacity_servings = capacity_servings
        self.food_category = food_category
        self.received_servings = 0

    # space left before the recipient is full
    def remaining_capacity(self):
        return self.capacity_servings - self.received_servings

    # the category rule plus free space decide
    def can_accept(self, donation):
        if self.food_category == "any" or self.food_category == donation.category:
            if self.remaining_capacity() > 0:
                return True
        return False
