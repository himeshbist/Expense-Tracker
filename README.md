# 💸  Personal Expense Tracker

An intuitive and powerful web application built with Python and Streamlit to help you take control of your finances. Track your daily expenses, visualize spending habits, set budgets, and gain actionable insights to manage your money effectively.

![App Screenshot](https://i.imgur.com/your_screenshot_url.png)
*Replace the URL above with a link to your app's screenshot. You can upload the `image_43ff62.png` file to a service like Imgur to get a URL.*

---

## ✨ Key Features

This application goes beyond simple expense logging. It's a full-featured financial dashboard designed for clarity and control.

-   📊 **Interactive Dashboard:** A clean, user-friendly interface to view all your financial data at a glance.
-   ✍️ **Effortless Expense Logging:** Quickly add, edit, or delete expenses with detailed fields for name, category, amount, date, and notes/tags.
-   📈 **Visual Analysis:** Instantly understand your spending distribution with an interactive pie chart and track your financial journey with a month-over-month spending bar chart.
-   🎯 **Category Budgeting:** Set monthly spending limits for different categories (e.g., Food, Transport) and monitor your progress with intuitive progress bars.
-   🔄 **Recurring Expense Management:** Automate the entry of fixed monthly payments like rent, subscriptions, or bills. Add them all for the current month with a single click.
-   📅 **Dynamic Filtering:** Filter your expenses by any date range to generate custom reports for a week, month, or year.
-   📝 **Notes & Tagging:** Add descriptions or tags (e.g., `#Vacation`, `#OfficeLunch`) to your expenses for powerful, specific filtering and analysis.
-   💾 **Persistent Storage:** All your data is securely saved in a local SQLite database, so you never lose your financial history.
-   📤 **Export to CSV:** Download your filtered expense data to a CSV file for your own records or for use in other applications like Excel or Google Sheets.

---

## 🛠️ Tech Stack

-   **Backend:** Python
-   **Web Framework:** Streamlit
-   **Data Manipulation:** Pandas
-   **Data Visualization:** Plotly Express
-   **Database:** SQLite

---

## 🚀 Getting Started

Follow these simple steps to get the application running on your local machine.

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    Create a file named `requirements.txt` and add the following lines:
    ```
    streamlit
    pandas
    plotly
    ```
    Then, run the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Your web browser will automatically open a new tab with the running application!

---

## 📂 Project Structure

