class DeclaredValue:
    def __init__(self, value, percent):
        self.value = value
        self.percent = percent

    def cost(self):
        if self.value:
            return self.value * self.percent / 100
        else:
            return 0  # avoid error if declared value is absent


"""
за письмо cost_per_letter
за объявленную ценность cost
стоимость пересылки cost_of_delivery
"""
