notification_list = [0.65, 2.10, 0.45]


def notification_cost(notification):
    print("обратились к функции notification_cost")
    match notification:
        case 1: return notification_list[0]
        case 2: return notification_list[1]
        case 3: return notification_list[2]
        case 4: return 0
