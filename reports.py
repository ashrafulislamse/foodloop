# FoodLoop report screens and display helpers

# print the titled separator used on every screen
def print_header(title):
    print()
    print("===============================")
    print(title)
    print("===============================")

# selection sort by expiry days, most urgent first
def sort_inventory(donations):
    result = []
    for d in donations:
        result.append(d)
    i = 0
    while i < len(result):
        smallest = i
        j = i + 1
        while j < len(result):
            if result[j].expiry_days < result[smallest].expiry_days:
                smallest = j
            j = j + 1
        if smallest != i:
            temp = result[i]
            result[i] = result[smallest]
            result[smallest] = temp
        i = i + 1
    return result

# show every donation ranked by expiry urgency
def view_inventory(donations):
    print_header("FOOD INVENTORY - MOST URGENT FIRST")
    if len(donations) == 0:
        print("No donations recorded yet.")
        return
    ordered = sort_inventory(donations)
    count = 1
    for d in ordered:
        if d.is_expired():
            print(f"{count}. {d.food_name} from {d.donor} - {d.servings} servings - {d.urgency_label()}")
        else:
            print(f"{count}. {d.food_name} from {d.donor} - {d.servings} servings - {d.urgency_label()} ({d.expiry_days} days left)")
        count = count + 1

# show only the donations of one category
def search_inventory(donations, category):
    print_header(f"SEARCH RESULTS - {category.upper()} FOOD")
    found = 0
    for d in donations:
        if d.category == category:
            if d.is_expired():
                print(f"{d.food_name} from {d.donor} - {d.servings} servings - {d.urgency_label()}")
            else:
                print(f"{d.food_name} from {d.donor} - {d.servings} servings - {d.urgency_label()} ({d.expiry_days} days left)")
            found = found + 1
    if found == 0:
        print(f"No {category} food in the inventory right now.")

# recommend the eligible recipient with the most free space
def match_donation(donations, recipients):
    print_header("MATCH A DONATION TO A RECIPIENT")
    # only non expired donations can be matched
    available = []
    for d in donations:
        if d.is_expired() == False:
            available.append(d)
    if len(available) == 0:
        print("No usable donations right now.")
        return
    count = 1
    for d in available:
        print(f"{count}. {d.food_name} - {d.servings} servings from {d.donor} ({d.category})")
        count = count + 1
    pick = input("Enter donation number to match: ")
    while pick.isdigit() == False or int(pick) < 1 or int(pick) > len(available):
        print("Invalid choice, try again.")
        pick = input("Enter donation number to match: ")
    donation = available[int(pick) - 1]
    # pick the eligible recipient with the largest remaining space
    best = ""
    for r in recipients:
        if r.can_accept(donation):
            if best == "":
                best = r
            elif r.remaining_capacity() > best.remaining_capacity():
                best = r
    if best == "":
        print("No eligible recipient found for this donation.")
    else:
        print(f"Match found: {donation.food_name} ({donation.servings} servings) can go to {best.name}")
        print(f"Reason: accepts {best.food_category} food and can take up to {best.remaining_capacity()} servings")

# collected, redistributed and still in stock, all reconciled
def impact_report(donations, distributions):
    print_header("IMPACT REPORT")
    # stock reconciliation: collected = still in inventory + distributed
    in_inventory = 0
    for d in donations:
        in_inventory = in_inventory + d.servings
    total_distributed = 0
    for d in distributions:
        total_distributed = total_distributed + d["servings"]
    collected = in_inventory + total_distributed
    print(f"Total food collected: {collected} servings")
    print(f"Food allocated: {total_distributed} servings")
    print(f"Food still in inventory: {in_inventory} servings")
    # expired batches remain in the inventory count but can never be handed out
    usable = 0
    for d in donations:
        if d.is_expired() == False:
            usable = usable + d.servings
    print(f"Food usable for distribution (not expired): {usable} servings")
    if collected > 0:
        # distribution rate as a percentage with one decimal
        rate = round(total_distributed * 100 / collected, 1)
        print(f"Distribution rate: {rate} percent")
    # recipients served, unique names through parallel lists
    served = []
    for d in distributions:
        name = d["recipient"]
        position = -1
        i = 0
        while i < len(served):
            if served[i] == name:
                position = i
            i = i + 1
        if position == -1:
            served.append(name)
    print(f"Recipient organisations with recorded allocations: {len(served)}")
    for name in served:
        print(f" - {name}")
    # batches that must move soon, named so volunteers can act on them
    urgent = []
    for d in donations:
        if d.is_expired() == False and d.expiry_days <= 2:
            urgent.append(d)
    print(f"Batches needing urgent distribution: {len(urgent)}")
    for d in urgent:
        print(f" - {d.food_name} from {d.donor} ({d.expiry_days} days left)")
    print("Every serving allocated is one step closer to SDG 2: Zero Hunger")

# servings given per donor across the whole session and the top donor
def donor_report(contributions):
    print_header("DONOR CONTRIBUTION REPORT")
    if len(contributions) == 0:
        print("No donations recorded yet, so no contributions to report.")
        return
    # parallel lists: donor names and what they gave in total
    names = []
    totals = []
    counts = []
    for c in contributions:
        name = c["donor"]
        position = -1
        i = 0
        while i < len(names):
            if names[i] == name:
                position = i
            i = i + 1
        if position == -1:
            names.append(name)
            totals.append(c["servings"])
            counts.append(1)
        else:
            totals[position] = totals[position] + c["servings"]
            counts[position] = counts[position] + 1
    # print every donor with a while loop over the parallel lists
    count = 1
    i = 0
    while i < len(names):
        word = "donations"
        if counts[i] == 1:
            word = "donation"
        print(f"{count}. {names[i]} - {totals[i]} servings across {counts[i]} {word}")
        count = count + 1
        i = i + 1
    top = 0
    top_name = ""
    i = 0
    while i < len(names):
        if totals[i] > top:
            top = totals[i]
            top_name = names[i]
        i = i + 1
    print(f"Top donor: {top_name} with {top} servings donated")
