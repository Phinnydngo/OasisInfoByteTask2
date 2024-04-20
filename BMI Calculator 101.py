import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BMI_Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.grid(row=0, column=0)
        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=0, column=1)

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.grid(row=1, column=0)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=3, columnspan=2)

        self.save_button = tk.Button(master, text="Save Data", command=self.save_data)
        self.save_button.grid(row=4, columnspan=2)

        self.load_button = tk.Button(master, text="Load Data", command=self.load_data)
        self.load_button.grid(row=5, columnspan=2)

        self.conn = sqlite3.connect('bmi_data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")
            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            self.result_label.config(text=f"BMI: {bmi:.2f}, Category: {category}")
            self.plot_bmi_data()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def get_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS bmi (
                        id INTEGER PRIMARY KEY,
                        weight REAL,
                        height REAL,
                        bmi REAL
                        )''')
        self.conn.commit()

    def save_data(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")
            bmi = weight / (height ** 2)
            self.c.execute("INSERT INTO bmi (weight, height, bmi) VALUES (?, ?, ?)", (weight, height, bmi))
            self.conn.commit()
            messagebox.showinfo("Success", "Data saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_data(self):
        self.c.execute("SELECT * FROM bmi")
        data = self.c.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No data to display.")
            return
        weights = [row[1] for row in data]
        heights = [row[2] for row in data]
        bmis = [row[3] for row in data]

        plt.figure(figsize=(8, 6))
        plt.scatter(weights, heights, c=bmis, cmap='viridis')
        plt.colorbar(label='BMI')
        plt.xlabel('Weight (kg)')
        plt.ylabel('Height (m)')
        plt.title('BMI Data')
        plt.grid(True)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, columnspan=2)

    def plot_bmi_data(self):
        self.c.execute("SELECT * FROM bmi")
        data = self.c.fetchall()
        if not data:
            return
        bmis = [row[3] for row in data]

        plt.figure(figsize=(6, 4))
        plt.hist(bmis, bins=10, edgecolor='black')
        plt.xlabel('BMI')
        plt.ylabel('Frequency')
        plt.title('BMI Distribution')
        plt.grid(True)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, columnspan=2)


def main():
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
