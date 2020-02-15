def convert_st_and_lb_to_kg(st_weight, lb_weight):
    return round((st_weight + lb_weight / 14) * 6.35, 1)


def convert_kg_to_st(kg_weight):
    return round((kg_weight//6.35), 0), round(((kg_weight/6.35)-(kg_weight//6.35))*14, 1)


def convert_cm_to_ft_and_in(cm_height):
    return round((cm_height * 0.3937)//12, 0), round((cm_height * 0.3937) % 12, 1)


def convert_ft_and_in_to_cm(feet_height, inch_height):
    return round(((feet_height * 12) + inch_height) * 2.54, 1)


def convert_lb_to_kg(lb_weight):
    return round(lb_weight*0.454, 1)
