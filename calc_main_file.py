import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msb
import os

from calc_sub_file import Metric
from calc_sub_file import Validator
import tkinter.filedialog as fd
import csv
import conversions_file
from datetime import datetime


class BmiCalc(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        BmiFrame(parent).grid(row=0, column=0)


class BmiFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        self.data_list = []
        self.file_name = None
        self.saved = False
        self.time_date = None
        self.headers_added = False

        self.metric = Metric()

        self.user_name = tk.StringVar()
        self.kg_weight = tk.StringVar()
        self.cm_height = tk.StringVar()
        self.time_date = tk.StringVar()

        self.st_weight = tk.StringVar()
        self.lb_weight = tk.StringVar()
        self.feet_height = tk.StringVar()
        self.inch_height = tk.StringVar()

        self.bmi = tk.StringVar()
        self.bmi_category = tk.StringVar()

        self.init_components()

    def init_components(self):  # Displaying the grid of labels and text entry fields
        ttk.Label(self, text="Your Name: ").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.user_name).grid(
            column=1, row=0)
        ttk.Label(self, text="Your Weight (kg):").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.kg_weight).grid(
            column=1, row=1)

        ttk.Label(self, text="Your Height (cm):").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.cm_height).grid(
            column=1, row=2)

        ttk.Label(self, text="Your Weight (st.):").grid(
            column=2, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.st_weight).grid(
            column=3, row=1)
        ttk.Label(self, text="Your Weight (lb):").grid(
            column=2, row=2, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.lb_weight).grid(
            column=3, row=2)

        ttk.Label(self, text="Your Height (ft):").grid(
            column=2, row=3, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.feet_height).grid(
            column=3, row=3)
        ttk.Label(self, text="Your Height (in):").grid(
            column=2, row=4, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.inch_height).grid(
            column=3, row=4)

        ttk.Label(self, text="Your BMI:").grid(
            column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.bmi,
                  state="readonly").grid(
            column=1, row=3)

        ttk.Label(self, text="Your BMI Category:").grid(
            column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.bmi_category,
                  state="readonly").grid(
            column=1, row=4)

        self.make_buttons()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def make_buttons(self):  # Creating buttons
        button_frame = ttk.Frame(self)

        button_frame.grid(column=0, row=5, columnspan=2, sticky=tk.E)
        ttk.Button(text="Exit", command=self.on_closing).grid(
            row=1, column=1, sticky=tk.E, padx=5, pady=5)

        ttk.Button(button_frame, text="Clear", command=self.clear) \
            .grid(column=0, row=0)
        ttk.Button(button_frame, text="Calculate", command=self.calculate) \
            .grid(column=1, row=0)

        ttk.Button(button_frame, text="Add", command=self.add_to_list) \
            .grid(row=1, column=1, sticky=tk.W, padx=0, pady=0)

        ttk.Button(button_frame, text="Save As...", command=self.save_as) \
            .grid(row=2, column=1, sticky=tk.W, padx=0, pady=0)

        ttk.Button(button_frame, text="Save", command=self.save) \
            .grid(row=1, column=0, sticky=tk.W, padx=15, pady=0)

        ttk.Button(button_frame, text="Open File...", command=self.read_from_file) \
            .grid(row=2, column=0, sticky=tk.W, padx=15, pady=0)

    def add_to_list(self):  # Reads data from GUI and adds each record to data_list[]
        empty_entries = True
        if self.user_name.get() == '' and self.kg_weight.get() == '' and self.cm_height.get() == '':
            msb.showerror("Empty Record - Nothing to Add", "Please complete your record with valid entries")
        elif self.user_name.get() == '':
            msb.showerror("User Name Missing", "Please add a user name to proceed")
        elif self.kg_weight.get() == '':
            msb.showerror("Weight Value Missing", "Please add a weight value to proceed")
        elif self.cm_height.get() == '':
            msb.showerror("Height Value Missing", "Please add a height value to proceed")
        else:
            empty_entries = False
        if not empty_entries and Validator.validate_name(self.user_name.get()) is not False and Validator\
                .validate_metric_weight(self.kg_weight.get()) is not False and Validator.validate_metric_height(
                self.cm_height.get()) is not False:
            if self.bmi.get() != "":
                self.saved = False
                now = datetime.now()
                self.time_date = now.strftime("%d/%m/%Y  %H:%M:%S")
                record = (self.user_name.get(), self.kg_weight.get(),
                          self.cm_height.get(), self.time_date)
                self.data_list.append(record)
                msb.showinfo("Record Added", "One Record Added")
                self.clear()
            else:
                msb.showerror("Unable to Add Entries", "Please calculate your bmi before adding your entries")

    def save_as(self):  # Saves data from GUI to a new file name after a data_list was created
        try:
            if not len(self.data_list) == 0:
                self.file_name = fd.asksaveasfilename(defaultextension=".csv",
                                                      filetypes=[("csv files", ".csv"), ("all files", ".*")])
                self.write_to_file()
                self.saved = True
            else:
                msb.showerror("Nothing to Save", "Please complete your data and click 'Add' before saving")
        except FileNotFoundError:
            msb.showinfo("File Not Saved", "You have not saved your file")

    def save(self):  # Saves data from GUI to an existing file name after a data_list was created
        if self.file_name is None or self.file_name == "":
            self.save_as()
        else:
            self.write_to_file()
            self.saved = True
            msb.showinfo("File Saved", "Your file has now been saved")

    def write_to_file(self):  # Writes the contents of a data_list from GUI to a file
        if len(self.data_list) > 0:
            csv_file = open(file=self.file_name, mode='w', newline='\n')
            writer = csv.writer(csv_file, delimiter=",")

            if not self.headers_added:  # Adding headers
                headers = ('Name', 'Weight (Kg)', 'Height (cm)', 'Date & Time')
                self.data_list.insert(0, headers)
                self.headers_added = True
                        
            for lcv in range(0, len(self.data_list)):
                writer.writerow(self.data_list[lcv])
            csv_file.close()
        else:
            msb.showwarning("Nothing to Save", "There are no records to save")

    def read_from_file(self):  # Reads a saved file
        self.file_name = fd.askopenfilename(defaultextension=".csv",
                                            filetypes=[("csv files", ".csv"), ("all files", ".*")])
        os.startfile(self.file_name)

    def read_weight(self):  # Reads and filters user weight entries, returns weight in kgs
        kg = self.kg_weight.get()
        st = self.st_weight.get()
        lb = self.lb_weight.get()

        if kg != "":
            if st != "" or lb != "":
                msb.showerror("Unable to Process Data",
                              "Please select either the Metric or Imperial system to process weight values")
                return False
            else:
                if (kg.replace('.', '', 1)).replace('e+', '', 1).isdigit():
                    return kg

                msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
                return False

        if st != "" or lb != "":
            if kg != "":
                msb.showerror("Unable to Process Data",
                              "Please select either the Metric or Imperial system to process weight values")
                return False
            else:
                if st != "" and lb != "":
                    if not (st.replace('.', '', 1)).replace('e+', '', 1).isdigit():
                        msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
                        return False
                    if not (lb.replace('.', '', 1)).replace('e+', '', 1).isdigit():
                        msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
                        return False
                    kg = conversions_file.convert_st_and_lb_to_kg(float(st), float(lb))
                elif st != "":
                    if not (st.replace('.', '', 1)).replace('e+', '', 1).isdigit():
                        msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
                        return False
                    kg = conversions_file.convert_st_and_lb_to_kg(float(st), 0)
                elif lb != "":
                    if not (lb.replace('.', '', 1)).replace('e+', '', 1).isdigit():
                        msb.showerror("Invalid Weight Value(s) Entered", "Weight values must be entirely numeric")
                        return False
                    kg = conversions_file.convert_lb_to_kg(float(lb))

        if kg == "" and st == "" and lb == "":
            msb.showerror("No Weight Entered", "Please enter valid weight value(s) to proceed")
            return False

        return kg

    def read_height(self):  # Reads and filters user height entries, returns height in cms
        cm = self.cm_height.get()
        ft = self.feet_height.get()
        inch = self.inch_height.get()

        if cm != "":
            if cm == "0":
                msb.showerror("Height Value Out of Range",
                              "Height values must be between 50-300 cm / 19.8 in-9 ft 10 in")
                return False
            if ft != "" or inch != "":
                msb.showerror("Unable to Process Data",
                              "Please select either the Metric or Imperial system to process height values")
                return False
            else:
                if not ((cm.replace('.', '', 1)).replace('e+', '', 1).isdigit()):
                    msb.showerror("Invalid Height Value(s) Entered", "Height values must be entirely numeric")
                    return False

        if ft != "" or inch != "":
            if cm != "":
                msb.showerror("Unable to Process Data",
                              "Please select either the Metric or Imperial system to process height values")
                return False
            else:
                if ft != "" and inch != "":
                    if ft == "0" and inch == "0":
                        msb.showerror("Height Value Out of Range",
                                      "Height values must be between 50-300 cm / 19.8 in-9 ft 10 in")
                        return False
                    if not ((ft.replace('.', '', 1)).replace('e+', '', 1).isdigit()) or not ((inch.replace('.', '', 1)).
                       replace('e+', '', 1).isdigit()):
                        msb.showerror("Invalid Height Value(s) Entered", "Height values must be entirely numeric")
                        return False
                    cm = conversions_file.convert_ft_and_in_to_cm(float(ft), float(inch))

                elif ft != "":
                    if ft == "0":
                        msb.showerror("Height Value Out of Range",
                                      "Height values must be between 50-300 cm / 19.8 in-9 ft 10 in")
                        return False
                    if not ((ft.replace('.', '', 1)).replace('e+', '', 1).isdigit()):
                        msb.showerror("Invalid Height Value(s) Entered", "Height values must be entirely numeric")
                        return False
                    cm = conversions_file.convert_ft_and_in_to_cm(float(ft), 0)
                elif inch != "":
                    if inch == "0":
                        msb.showerror("Height Value Out of Range",
                                      "Height values must be between 50-300 cm / 19.8 in-9 ft 10 in")
                        return False
                    if not ((inch.replace('.', '', 1)).replace('e+', '', 1).isdigit()):
                        msb.showerror("Invalid Height Value(s) Entered", "Height values must be entirely numeric")
                        return False
                    cm = conversions_file.convert_ft_and_in_to_cm(0, float(inch))

        if cm == "" and ft == "" and inch == "":
            msb.showerror("No Height Entered", "Please enter valid height value(s) to proceed")
            return False
        
        return cm

    def calculate(self):  # Calculates the bmi based on self declared data and given exceptions
        go_again = True
        valid_weight = True
        valid_height = True
        while go_again and (valid_weight and valid_height):

            name_value = str(self.user_name.get())
            Validator.validate_name(name_value)

            weight_value = self.read_weight()
            height_value = self.read_height()

            if not weight_value:
                valid_weight = False
            else:
                valid_weight = Validator.validate_metric_weight(float(weight_value))
                if valid_weight is None:
                    valid_weight = True

            if not height_value:
                valid_height = False
            else:
                valid_height = Validator.validate_metric_height(float(height_value))
                if valid_height is None:
                    valid_height = True

            if not valid_weight or not valid_height:
                break

            st, p = conversions_file.convert_kg_to_st(float(weight_value))
            if self.kg_weight.get() == "":
                self.kg_weight.set(float(weight_value))
            if self.st_weight.get() == "" and self.lb_weight.get() == "":
                self.st_weight.set(st)
                self.lb_weight.set(p)

            self.metric.kg_weight = float(self.kg_weight.get())

            feet, inch = conversions_file.convert_cm_to_ft_and_in(float(height_value))
            if self.cm_height.get() == "":
                self.cm_height.set(float(height_value))
            if self.feet_height.get() == "" and self.inch_height.get() == "":
                self.feet_height.set(feet)
                self.inch_height.set(inch)

            self.metric.cm_height = float(self.cm_height.get())

            go_again = False
            if valid_weight is not False and valid_height is not False:
                try:
                    self.bmi.set(float(self.metric.calculate_metric_bmi()))
                    self.bmi_category.set(str(self.metric.categorize_bmi()))
                except ZeroDivisionError:
                    msb.showerror("Height Value Out of Range",
                                  "Height values must be between 50-300 cm / 19.8 in-9 ft 10 in")

    def clear(self):  # Clears data
        self.user_name.set("")
        self.kg_weight.set("")
        self.cm_height.set("")

        self.inch_height.set("")
        self.feet_height.set("")
        self.st_weight.set("")
        self.lb_weight.set("")

        self.bmi.set("")
        self.bmi_category.set("")

    def on_closing(self):  # Application's closure under conditions
        if not self.saved:
            if msb.askyesnocancel("File Not Saved", "Are you sure you want to quit without saving?"):
                root.destroy()
        elif msb.askyesnocancel("Quit Application", "Are you sure you want to quit?"):
            root.destroy()


path = './bmi_pic4.png'

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tom's BMI Calculator - "
               "Enter name followed by weight in kilograms/stone&pounds and height in centimetres/feet&inches")
    BmiCalc(root)
    root.mainloop()
