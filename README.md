#  Advanced Personal Expense Tracker

An intuitive and powerful web application built with **Python** and **Streamlit** to help you take control of your finances.
Easily track expenses, visualize spending habits, set budgets, and gain actionable insights to manage your money effectively.

[👉 **View Live App**](https://expense-tracker-proj.streamlit.app/?embed_options=light_theme,show_colored_line,disable_scrolling,show_padding,dark_theme)



---

## ✨ Features

This application goes beyond simple expense logging – it’s a **full-featured financial dashboard** built for clarity and control:

* 📊 **Interactive Dashboard** – View all your financial data at a glance in a clean, user-friendly interface.
* ✍️ **Effortless Expense Logging** – Add, edit, or delete expenses with details like name, category, amount, date, and notes/tags.
* 📈 **Visual Analysis** – Interactive pie chart for spending distribution + bar chart for month-over-month spending.
* 🎯 **Category Budgeting** – Set monthly budgets by category (Food, Transport, etc.) and monitor progress with progress bars.
* 🔄 **Recurring Expense Management** – Automate fixed monthly payments (rent, subscriptions, bills) with a single click.
* 📅 **Dynamic Filtering** – Generate custom reports for any date range (week, month, year).
* 📝 **Notes & Tags** – Add custom tags (e.g., `#Vacation`, `#OfficeLunch`) for advanced filtering.
* 💾 **Persistent Storage** – Data saved in local **SQLite** database (no risk of losing history).
* 📤 **Export to CSV** – Download filtered data for Excel/Google Sheets analysis.

---

## 🛠️ Tech Stack

* **Frontend / Web Framework:** [Streamlit](https://streamlit.io/)
* **Backend / Database:** SQLite
* **Data Analysis:** Pandas
* **Data Visualization:** Plotly Express

---

## 🚀 Getting Started

Follow these steps to run the application locally:

### ✅ Prerequisites

* Python **3.8+**
* `pip` (Python package installer)

### ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/himeshbist/Expense-Tracker.git
   cd Expense-Tracker
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```

   Your browser will open automatically with the app running! 🎉

---

## 📂 Project Structure

```
Expense-Tracker/
├── app.py                  # Main Streamlit application
├── expenses_advanced.db    # SQLite database (auto-generated)
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## 🌟 Future Enhancements

Planned improvements for upcoming versions:

* ☁️ **Cloud Data Sync** – Sync data with Firebase/Supabase for multi-device access.
* 🤖 **AI Insights** – Get personalized suggestions based on spending habits.
* 👥 **Multi-User Authentication** – Secure login for multiple users.
* 📑 **Enhanced Reporting** – Auto-generate & email PDF financial reports.

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

### 🙌 Contribution & Feedback

Contributions are welcome! Feel free to open issues or submit pull requests.
If you like this project, don’t forget to ⭐ the repo 😊

---
