from services.sheets import save_to_sheet
leads = []

def save_lead(user):
    print("NEW LEAD:", user)

    save_to_sheet(user) 