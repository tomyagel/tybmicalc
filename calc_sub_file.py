import tkinter.messagebox as msb


class Validator:

    @classmethod
    def validate_name(cls, name):  # Validates the name entry
        str_name = str(name)
        if str_name == '':
            msb.showerror("No Name Entered", "Please enter a name to proceed")
            return False
        if not str_name.isalpha():
            msb.showerror("Invalid Name Entered", "Your name entry must be entirely alphabetic")
            return False

    @classmethod
    def validate_metric_weight(cls, kg_weight):  # Validates the weight entry
        str_kg_weight = str(kg_weight)
        if str_kg_weight == '':
            msb.showerror("No Weight Entered", "Please enter valid weight value(s) to proceed")
            return False
        if not (str_kg_weight.replace('.', '', 1)).replace('e+', '', 1).isdigit():
            msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
            return False
        if float(kg_weight) < 2 or float(kg_weight) > 700:
            msb.showerror("Weight Value Out of Range", "Weight values must be between 2-700 kg / 4.5 lbs-110 st. 3.3lbs")
            return False

    @classmethod
    def validate_metric_height(cls, cm_height):  # Validates the height entry
        str_cm_height = str(cm_height)
        if str_cm_height == '':
            msb.showerror("No Height Entered", "Please enter valid height value(s) to proceed")
            return False
        if not (str_cm_height.replace('.', '', 1)).replace('e+', '', 1).isdigit():
            msb.showerror("Invalid Height Value(s) Entered", "Height values must be entirely numeric")
            return False
        if (float(cm_height) != 0.0 and float(cm_height) < 50) or float(cm_height) > 300:
            msb.showerror("Height Value Out of Range",
                          "Height values must be between 50-300 cm / 19.7 in-9 ft 11 in")
            return False


class Metric:

    def __init__(self):
        self.user_name = ""
        self.kg_weight = 0
        self.cm_height = 0

    def calculate_metric_bmi(self):
        kg_weight = self.kg_weight
        cm_height = self.cm_height

        bmi = 0
        bmi += kg_weight / ((cm_height / 100) * (cm_height / 100))
        bmi = round(bmi, 1)

        return bmi

    def categorize_bmi(self):
        kg_weight = self.kg_weight
        cm_height = self.cm_height

        bmi = 0
        bmi += kg_weight / ((cm_height/100) * (cm_height/100))
        bmi = round (bmi, 1)

        bmi_category = ""
        if bmi < 18.5:
            bmi_category += "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_category += "Normal (Healthy Weight)"
        elif 25 <= bmi < 30:
            bmi_category += "Overweight"
        else:
            bmi_category += "Obese"

        return bmi_category
