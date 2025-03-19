from pocket_app.models import ItemInstance

def calculate_balance(beepocket):
    if not beepocket:
        return 0

    balance = beepocket.starting_balance

    # Get all approved item instances for this BeePocket for balance calculation
    approved_item_instances = ItemInstance.objects.filter(
        BeePocketID=beepocket,
        Approved=True,
    )

    # Calculate balance
    for item in approved_item_instances:
        if item.item.item_type == 'Task':  # Pollen/Task (positive)
            balance += item.item.item_value
        # Sting/Consequence (negative)
        elif item.item.item_type == 'Consequence':
            balance -= item.item.item_value
        elif item.item.item_type == 'Reward':  # Honey/Reward (negative)
            balance -= item.item.item_value
        elif item.item.item_type == 'Adjustment':
            balance += item.item.item_value

    return balance