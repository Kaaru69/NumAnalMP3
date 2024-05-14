import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, simplify, latex
from fractions import Fraction

class ForexData:
    """
    A class to represent the Forex data and related operations.
    """
    def __init__(self, dates, exchange_rates):
        """
        Initialize the ForexData with dates and exchange rates.
        """
        self.dates = dates
        self.exchange_rates = exchange_rates
        self.date_values = [self.date_to_num(date) for date in self.dates]

    def lagrange_interpolation(self, x, x_data, y_data):
        """
        Calculates the Lagrange polynomial for a given x value.
        """
        n = len(x_data)
        result = 0
        for i in range(n):
            numerator = 1
            denominator = 1
            for j in range(n):
                if i != j:
                    numerator *= (x - x_data[j])
                    denominator *= (x_data[i] - x_data[j])
            result += y_data[i] * numerator / denominator
        return result

    def date_to_num(self, date_str):
        """
        Convert a date string to numerical value.
        """
        ref_date = datetime(2002, 1, 1)
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (target_date - ref_date).days

    def interpolate_exchange_rate(self, target_date_str):
        """
        Interpolate the exchange rate for a given date.
        """
        try:
            target_value = self.lagrange_interpolation(self.date_to_num(target_date_str), self.date_values, self.exchange_rates)
            return f"Interpolated exchange rate for {target_date_str}: {target_value:.4f}"
        except ValueError:
            return "Invalid date format. Please enter a date in YYYY-MM-DD format."

    def plot_exchange_rates(self):
        """
        Plot the exchange rates data.
        """
        plt.plot(self.dates, self.exchange_rates, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.title('U$ to PHP Forex Exchange Rate Interpolation')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

class ForexLagrangeApp:
    """
    A class to represent the combined Forex and Lagrange interpolation GUI using tkinter.
    """
    def __init__(self, root):
        """
        Initialize the GUI elements.
        """
        self.root = root
        self.root.title("Forex and Lagrange Interpolation")

        self.forex_data = ForexData(
            ["2002-01-01", "2002-02-01", "2002-03-01", "2002-04-01", "2002-05-01", "2002-06-01", "2002-07-01", "2002-08-01", "2002-09-01", "2002-10-01", "2002-11-01", "2002-12-01",
             "2003-01-01", "2003-02-01", "2003-03-01", "2003-04-01", "2003-05-01", "2003-06-01", "2003-07-01", "2003-08-01", "2003-09-01", "2003-10-01", "2003-11-01", "2003-12-01"],
            [26.5850, 26.2703, 26.7617, 27.2878, 27.3863, 28.6447, 28.0576, 28.0241, 28.5094, 29.0770, 29.9216, 30.1003, 31.1729, 32.1087, 32.8384, 32.1492, 34.0153, 35.4584,
             35.5996, 35.8302, 36.3606, 38.1060, 39.6118, 40.8515]
        )

        self.label = tk.Label(root, text="Enter a date (YYYY-MM-DD) for Forex interpolation:")
        self.label.pack()

        self.forex_entry = tk.Entry(root)
        self.forex_entry.pack()

        self.forex_button = tk.Button(root, text="Calculate Forex Rate", command=self.calculate_forex_rate)
        self.forex_button.pack()

        self.forex_plot_button = tk.Button(root, text="Plot Forex Data", command=self.forex_data.plot_exchange_rates)
        self.forex_plot_button.pack()

        tk.Label(root, text="Number of Points for Lagrange Interpolation:").pack()
        self.num_points_entry = tk.Entry(root)
        self.num_points_entry.pack()

        generate_button = tk.Button(root, text="Generate Points", command=self.generate_point_entries)
        generate_button.pack()

        tk.Label(root, text="X Value for Lagrange Interpolation:").pack()
        self.x_entry = tk.Entry(root)
        self.x_entry.pack()

        tk.Button(root, text="Interpolate Lagrange", command=self.interpolate_lagrange).pack()

        self.point_frames = []

        self.reset_button = tk.Button(root, text="Reset App", command=self.reset_app)
        self.reset_button.pack()

        self.clear_button = tk.Button(root, text="Clear Fields", command=self.clear_fields)
        self.clear_button.pack()

    def calculate_forex_rate(self):
        """
        Calculate the interpolated exchange rate.
        """
        target_date_str = self.forex_entry.get()
        result = self.forex_data.interpolate_exchange_rate(target_date_str)
        messagebox.showinfo("Forex Result", result)

    def generate_point_entries(self):
        num_points = int(self.num_points_entry.get())
        for frame in self.point_frames:
            frame.destroy()
        self.point_frames.clear()

        for i in range(num_points):
            point_frame = tk.Frame(self.root)
            point_frame.pack()

            label = tk.Label(point_frame, text=f"Point {i+1}:")
            label.pack(side="left")

            entry_x = tk.Entry(point_frame)
            entry_x.pack(side="left")

            entry_y = tk.Entry(point_frame)
            entry_y.pack(side="left")

            self.point_frames.append(point_frame)

    def reset_app(self):
        self.forex_entry.delete(0, 'end')
        self.x_entry.delete(0, 'end')
        for frame in self.point_frames:
            frame.destroy()
        self.point_frames.clear()

    def clear_fields(self):
        self.forex_entry.delete(0, 'end')
        self.x_entry.delete(0, 'end')
        for frame in self.point_frames:
            frame.destroy()
        self.point_frames.clear()

    def interpolate_lagrange(self):
        x_val = float(self.x_entry.get())
        points = self.get_points()
        if not points:
            return

        lagrange_poly = self.compute_lagrange_polynomial(points)
        result = lagrange_poly.subs({'x': x_val})

        polynomial_latex = latex(lagrange_poly)
        self.display_polynomial_in_popup(polynomial_latex)
        self.display_result(result, x_val)

    def get_points(self):
        points = []
        for frame in self.point_frames:
            entry_x = frame.winfo_children()[1]
            entry_y = frame.winfo_children()[2]
            try:
                x = Fraction(entry_x.get())
                y = Fraction(entry_y.get())
                points.append((x, y))
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all points")
                return None
        return points

    def compute_lagrange_polynomial(self, points):
        x, y = symbols('x y')
        lagrange_poly = 0
        for i in range(len(points)):
            numerator = 1
            denominator = 1
            for j in range(len(points)):
                if j != i:
                    numerator *= (x - points[j][0])
                    denominator *= (points[i][0] - points[j][0])
            lagrange_poly += (numerator / denominator) * points[i][1]

        return simplify(lagrange_poly)

    def display_polynomial_in_popup(self, polynomial_latex):
        popup = Toplevel()
        popup.title("Lagrange Polynomial")
        fig = plt.figure(figsize=(4, 1))
        plt.text(0.5, 0.5, f"${polynomial_latex}$", fontsize=12, ha='center', va='center')
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_result(self, result, x_val):
        msg = f"Result at x={x_val}: {result}"
        messagebox.showinfo("Lagrange Result", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForexLagrangeApp(root)
    root.mainloop()

# *eyy*
