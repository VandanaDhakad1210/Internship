import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# -----------------------------
# STEP 1: READ & ANALYZE DATA
# -----------------------------
data = pd.read_csv("sample.csv")

summary = data.groupby("Department")["Salary"].agg(["count", "mean", "min", "max"])
summary.reset_index(inplace=True)

# -----------------------------
# STEP 2: CREATE CHART
# -----------------------------
plt.figure(figsize=(6,4))
data.groupby("Department")["Salary"].mean().plot(kind='bar', color='skyblue')
plt.title("Average Salary by Department")
plt.ylabel("Salary")
plt.tight_layout()
chart_file = "salary_chart.png"
plt.savefig(chart_file)
plt.close()

# -----------------------------
# STEP 3: GENERATE PDF REPORT
# -----------------------------
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Employee Salary Report", ln=1, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_summary_table(self, summary_df):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Salary Summary by Department", ln=1)

        self.set_font("Arial", "", 11)
        col_widths = [40, 30, 30, 30, 30]
        headers = ["Department", "Count", "Average", "Min", "Max"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1)
        self.ln()

        for index, row in summary_df.iterrows():
            self.cell(col_widths[0], 8, str(row["Department"]), border=1)
            self.cell(col_widths[1], 8, str(row["count"]), border=1)
            self.cell(col_widths[2], 8, f"{row['mean']:.2f}", border=1)
            self.cell(col_widths[3], 8, f"{row['min']:.2f}", border=1)
            self.cell(col_widths[4], 8, f"{row['max']:.2f}", border=1)
            self.ln()

    def add_chart(self, chart_path):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Chart: Average Salary by Department", ln=1)
        self.image(chart_path, x=30, y=None, w=150)

# -----------------------------
# STEP 4: BUILD THE REPORT
# -----------------------------
pdf = PDFReport()
pdf.add_page()
pdf.add_summary_table(summary)
pdf.add_chart(chart_file)

output_file = "Employee_Salary_Report.pdf"
pdf.output(output_file)
print(f"PDF report generated: {output_file}")
