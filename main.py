# FoodLoop - Community Food Rescue and Redistribution Manager
# Final assessment - SDG 2: Zero Hunger
import reports
from models import Donation, Recipient
from data import get_sample_recipients, get_sample_donations

# print the menu shown before every choice
def show_menu():
    print()
    print("===============================")
    print("FOODLOOP - FOOD RESCUE MANAGER")
    print("SDG 2: ZERO HUNGER")
    print("===============================")
    print("1. Add recipient organisation")
    print("2. View recipient organisations")
    print("3. Record food donation")
    print("4. View food inventory")
    print("5. Search inventory by category")
    print("6. Match a donation to a recipient")
    print("7. Record a distribution")
    print("8. Impact report")
    print("9. Donor contribution report")
    print("0. Exit")

# keep asking until the field is not empty
def ask_nonempty(prompt):
    text = input(prompt)
    while text == "":
        print("This field cannot be empty.")
        text = input(prompt)
    return text

# keep asking until the value is a whole number above zero
def ask_positive_int(prompt):
    text = input(prompt)
    while text.isdigit() == False or int(text) == 0:
        print("Please enter a whole number above zero.")
        text = input(prompt)
    return int(text)

# keep asking until the category is a known one
def ask_category(prompt, allow_any):
    text = input(prompt).lower()
    if allow_any:
        while text != "cooked" and text != "raw" and text != "packed" and text != "any":
            print("Please type cooked, raw, packed or any.")
            text = input(prompt).lower()
    else:
        while text != "cooked" and text != "raw" and text != "packed":
            print("Please type cooked, raw or packed.")
            text = input(prompt).lower()
    return text

# register a new community organisation
def add_recipient(recipients):
    reports.print_header("ADD RECIPIENT ORGANISATION")
    name = ask_nonempty("Organisation name: ")
    org_type = ask_nonempty("Type of organisation (food bank / orphanage / welfare home): ")
    capacity = ask_positive_int("Storage capacity in servings: ")
    category = ask_category("Food category accepted (cooked / raw / packed / any): ", True)
    recipients.append(Recipient(name, org_type, capacity, category))
    print(f"Recipient added: {name}")

# list every recipient and the space it has left
def view_recipients(recipients):
    reports.print_header("RECIPIENT ORGANISATIONS")
    if len(recipients) == 0:
        print("No recipients recorded yet.")
        return
    count = 1
    for r in recipients:
        print(f"{count}. {r.name} ({r.org_type}) - {r.remaining_capacity()} of {r.capacity_servings} servings free - accepts {r.food_category}")
        count = count + 1

# record one food batch from a donor
def record_donation(donations):
    reports.print_header("RECORD FOOD DONATION")
    donor = ask_nonempty("Donor name: ")
    food = ask_nonempty("Food name: ")
    category = ask_category("Food category (cooked / raw / packed): ", False)
    servings = ask_positive_int("Number of servings: ")
    expiry = ask_positive_int("Days until expiry: ")
    donations.append(Donation(donor, food, category, servings, expiry))
    print(f"Donation recorded: {food} ({servings} servings, expires in {expiry} days)")

# move part of one batch to a recipient and update both records
def record_distribution(donations, distributions, recipients):
    reports.print_header("RECORD A DISTRIBUTION")
    # only non expired donations can be distributed
    usable = []
    for d in donations:
        if d.is_expired() == False:
            usable.append(d)
    if len(usable) == 0:
        print("No usable donations to distribute.")
        return
    count = 1
    for d in usable:
        print(f"{count}. {d.food_name} - {d.servings} servings from {d.donor}")
        count = count + 1
    pick = input("Donation number to distribute: ")
    while pick.isdigit() == False or int(pick) < 1 or int(pick) > len(usable):
        print("Invalid choice, try again.")
        pick = input("Donation number to distribute: ")
    donation = usable[int(pick) - 1]
    view_recipients(recipients)
    rpick = input("Recipient number: ")
    while rpick.isdigit() == False or int(rpick) < 1 or int(rpick) > len(recipients):
        print("Invalid choice, try again.")
        rpick = input("Recipient number: ")
    recipient = recipients[int(rpick) - 1]
    if recipient.can_accept(donation) == False:
        print(f"{recipient.name} cannot take this food (category full or not accepted).")
        return
    # allocation is capped by the batch size and the space the recipient has left
    limit = recipient.remaining_capacity()
    if donation.servings < limit:
        limit = donation.servings
    print(f"The batch holds {donation.servings} servings and {recipient.name} can take {recipient.remaining_capacity()}.")
    alloc = ask_positive_int(f"Servings to allocate (1 to {limit}): ")
    while alloc > limit:
        print(f"Allocation must be between 1 and {limit}.")
        alloc = ask_positive_int(f"Servings to allocate (1 to {limit}): ")
    # stock reconciliation: the batch shrinks, the recipient fills up
    donation.servings = donation.servings - alloc
    recipient.received_servings = recipient.received_servings + alloc
    distributions.append({"donor": donation.donor, "food": donation.food_name, "recipient": recipient.name, "servings": alloc})
    print(f"Distributed {alloc} servings of {donation.food_name} to {recipient.name}")
    if donation.servings == 0:
        print(f"The batch of {donation.food_name} is fully distributed and removed from the inventory.")
    else:
        print(f"{donation.servings} servings of {donation.food_name} remain in the inventory.")
    # remove fully used up batches
    i = 0
    while i < len(donations):
        if donations[i].servings == 0:
            del donations[i]
        else:
            i = i + 1

# load the sample data and run the menu loop
def main():
    recipients = get_sample_recipients()
    donations = get_sample_donations()
    distributions = []
    print("FOODLOOP - COMMUNITY FOOD RESCUE AND REDISTRIBUTION MANAGER")
    print("A final assessment application for SDG 2: Zero Hunger")
    choice = ""
    while choice != "0":
        show_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            add_recipient(recipients)
        elif choice == "2":
            view_recipients(recipients)
        elif choice == "3":
            record_donation(donations)
        elif choice == "4":
            reports.view_inventory(donations)
        elif choice == "5":
            category = ask_category("Search for which food category? ", False)
            reports.search_inventory(donations, category)
        elif choice == "6":
            reports.match_donation(donations, recipients)
        elif choice == "7":
            record_distribution(donations, distributions, recipients)
        elif choice == "8":
            reports.impact_report(donations, distributions)
        elif choice == "9":
            reports.donor_report(distributions)
        elif choice == "0":
            confirm = input("Exit FoodLoop? (y/n): ")
            if confirm == "y" or confirm == "yes":
                print("Thank you for rescuing food today.")
                choice = "0"
            else:
                choice = ""
        else:
            print("Invalid choice, please enter 0 to 9.")

main()
