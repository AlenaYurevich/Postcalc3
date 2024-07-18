notification_costs = {
    1: 0.65,
    2: 2.10,
    3: 0.45,
    4: 0.00,
}


def notification_cost(notification):
    if not isinstance(notification, int) or notification not in notification_costs:
        raise ValueError("Invalid notification type. Must be one of: 1, 2, 3, 4.")
    return notification_costs.get(notification)

# def notification_cost(notification):
#     print("обратились к функции notification_cost")
#     match notification:
#         case 1: return notification_list[0]
#         case 2: return notification_list[1]
#         case 3: return notification_list[2]
#         case 4: return 0


print(notification_cost(4))
