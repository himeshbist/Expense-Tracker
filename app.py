import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px
import json

# --- App Configuration ---
st.set_page_config(
    page_title="Advanced Expense Tracker",
    page_icon="💸",
    layout="wide"
)

# --- Database Setup ---
DB_FILE = "expenses_advanced.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the necessary database tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Main expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
    """)
    # Recurring expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            day_of_month INTEGER NOT NULL
        )
    """)
    # Category budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_budgets (
            category TEXT PRIMARY KEY,
            budget REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Expense Management Functions ---
def execute_query(query, params=(), fetch=None):
    """A helper function to execute database queries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch == 'one':
        result = cursor.fetchone()
    elif fetch == 'all':
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    conn.close()
    return result

def add_expense(name, category, amount, date, notes):
    execute_query("INSERT INTO expenses (name, category, amount, date, notes) VALUES (?, ?, ?, ?, ?)",
                  (name, category, amount, date, notes))

def get_expenses_as_df():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df

def update_expense(expense_id, name, category, amount, date, notes):
    execute_query("UPDATE expenses SET name=?, category=?, amount=?, date=?, notes=? WHERE id=?",
                  (name, category, amount, date.strftime('%Y-%m-%d'), notes, expense_id))

def delete_expense(expense_id):
    execute_query("DELETE FROM expenses WHERE id=?", (expense_id,))

# --- Recurring Expense Functions ---
def add_recurring_expense(name, category, amount, day):
    execute_query("INSERT INTO recurring_expenses (name, category, amount, day_of_month) VALUES (?, ?, ?, ?)",
                  (name, category, amount, day))

def get_recurring_expenses():
    return execute_query("SELECT * FROM recurring_expenses", fetch='all')

def delete_recurring_expense(rec_id):
    execute_query("DELETE FROM recurring_expenses WHERE id=?", (rec_id,))

# --- Category Budget Functions ---
def set_category_budget(category, budget):
    execute_query("INSERT OR REPLACE INTO category_budgets (category, budget) VALUES (?, ?)", (category, budget))

def get_category_budgets():
    return {row['category']: row['budget'] for row in execute_query("SELECT * FROM category_budgets", fetch='all')}

# --- Initialize Database ---
create_tables()

# --- Main Application UI ---
st.title("💸 Advanced Personal Expense Tracker")
st.markdown("Your all-in-one dashboard to manage finances, track trends, and stay on budget.")

# --- Sidebar ---
st.sidebar.header("Actions")
app_mode = st.sidebar.selectbox("Choose a section", ["Dashboard", "Manage Recurring Expenses", "Set Category Budgets"])

# --- Global elements ---
EXPENSE_CATEGORIES = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc", "🚗 Transport", "💡 Utilities", "🏥 Healthcare"]

if app_mode == "Dashboard":
    # --- Add Expense Form in Sidebar ---
    st.sidebar.markdown("---")
    st.sidebar.header("Add New Expense")
    with st.sidebar.form("expense_form", clear_on_submit=True):
        expense_name = st.text_input("Expense Name", placeholder="e.g., Coffee")
        expense_amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        expense_date = st.date_input("Date", datetime.now())
        expense_category = st.selectbox("Category", EXPENSE_CATEGORIES)
        expense_notes = st.text_area("Notes / Tags", placeholder="e.g., #OfficeLunch, Meeting with client")
        
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if not expense_name or expense_amount <= 0:
                st.sidebar.warning("Please fill in all fields with valid values.")
            else:
                add_expense(expense_name, expense_category, expense_amount, expense_date.strftime('%Y-%m-%d'), expense_notes)
                st.sidebar.success(f"Expense '{expense_name}' added successfully!")
                st.rerun()

    # --- Main Dashboard Display ---
    expenses_df = get_expenses_as_df()

    if expenses_df.empty:
        st.info("No expenses recorded yet. Add your first expense or manage recurring ones from the sidebar.")
    else:
        # --- Date Filtering ---
        st.header("Filter Your Expenses")
        min_date = expenses_df['date'].min().date()
        max_date = expenses_df['date'].max().date()
        
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = col2.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

        filtered_df = expenses_df[(expenses_df['date'].dt.date >= start_date) & (expenses_df['date'].dt.date <= end_date)]

        if filtered_df.empty:
            st.warning("No expenses found in the selected date range.")
        else:
            # --- Metrics ---
            total_spent = filtered_df["amount"].sum()
            st.header(f"Spending Summary: {start_date.strftime('%b %d')} to {end_date.strftime('%b %d')}")
            st.metric("Total Spent", f"₹{total_spent:,.2f}")
            
            # --- Visualizations ---
            st.markdown("---")
            st.header("Visual Analysis")
            tab1, tab2 = st.tabs(["Spending Distribution", "Monthly Trends"])

            with tab1:
                fig_pie = px.pie(filtered_df, names='category', values='amount', title='Spending by Category', hole=0.4)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

            with tab2:
                monthly_spending = expenses_df.copy()
                monthly_spending['month'] = monthly_spending['date'].dt.to_period('M').astype(str)
                monthly_summary = monthly_spending.groupby('month')['amount'].sum().reset_index()
                fig_bar = px.bar(monthly_summary, x='month', y='amount', title='Total Spending Per Month', labels={'month': 'Month', 'amount': 'Total Spent (₹)'})
                st.plotly_chart(fig_bar, use_container_width=True)

            # --- Category Budget Progress ---
            st.markdown("---")
            st.header("Category Budget Tracker")
            category_budgets = get_category_budgets()
            if not category_budgets:
                st.info("No category budgets set. Go to 'Set Category Budgets' to add them.")
            else:
                current_month_df = filtered_df[filtered_df['date'].dt.month == datetime.now().month]
                category_spending = current_month_df.groupby('category')['amount'].sum()
                for category, budget in category_budgets.items():
                    spent = category_spending.get(category, 0)
                    progress = min(spent / budget, 1.0) if budget > 0 else 0
                    st.write(f"**{category}**: ₹{spent:,.2f} / ₹{budget:,.2f}")
                    st.progress(progress)

            # --- Expense Data Table with Edit/Delete ---
            st.markdown("---")
            st.header("Expense Details")
            for i in filtered_df.index:
                exp = filtered_df.loc[i]
                with st.expander(f"{exp['date'].strftime('%Y-%m-%d')} - {exp['name']} (₹{exp['amount']:.2f})"):
                    with st.form(f"edit_form_{exp['id']}"):
                        st.write(f"Editing Expense ID: {exp['id']}")
                        edit_name = st.text_input("Name", value=exp['name'], key=f"name_{exp['id']}")
                        edit_amount = st.number_input("Amount", value=exp['amount'], key=f"amount_{exp['id']}")
                        edit_date = st.date_input("Date", value=exp['date'], key=f"date_{exp['id']}")
                        edit_category = st.selectbox("Category", EXPENSE_CATEGORIES, index=EXPENSE_CATEGORIES.index(exp['category']), key=f"cat_{exp['id']}")
                        edit_notes = st.text_area("Notes", value=exp['notes'], key=f"notes_{exp['id']}")
                        
                        col_save, col_delete, _ = st.columns([1,1,5])
                        if col_save.form_submit_button("Save"):
                            update_expense(exp['id'], edit_name, edit_category, edit_amount, edit_date, edit_notes)
                            st.success("Expense updated!"); st.rerun()
                        if col_delete.form_submit_button("Delete"):
                            delete_expense(exp['id']); st.warning("Expense deleted!"); st.rerun()
            
            # --- Export Data to CSV ---
            st.markdown("---")
            st.header("Export Data")
            csv = filtered_df[['date', 'name', 'category', 'amount', 'notes']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Expenses as CSV",
                data=csv,
                file_name=f'expenses_{start_date}_to_{end_date}.csv',
                mime='text/csv',
            )


elif app_mode == "Manage Recurring Expenses":
    st.header("Manage Recurring Expenses")
    st.write("Add expenses that occur regularly, like rent or subscriptions.")

    with st.form("recurring_form", clear_on_submit=True):
        rec_name = st.text_input("Expense Name")
        rec_amount = st.number_input("Amount (₹)")
        rec_category = st.selectbox("Category", EXPENSE_CATEGORIES)
        rec_day = st.number_input("Day of Month", min_value=1, max_value=31, step=1)
        if st.form_submit_button("Add Recurring Expense"):
            add_recurring_expense(rec_name, rec_category, rec_amount, rec_day)
            st.success(f"Added '{rec_name}' to recurring expenses.")
            st.rerun()
    
    st.markdown("---")
    recurring_expenses = get_recurring_expenses()
    if recurring_expenses:
        st.subheader("Current Recurring Expenses")
        for rec in recurring_expenses:
            col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])
            col1.write(rec['name'])
            col2.write(rec['category'])
            col3.write(f"₹{rec['amount']:.2f}")
            col4.write(f"Day: {rec['day_of_month']}")
            if col5.button("Delete", key=f"del_rec_{rec['id']}"):
                delete_recurring_expense(rec['id']); st.rerun()
        
        st.markdown("---")
        if st.button("Add This Month's Recurring Expenses"):
            today = datetime.now()
            for rec in recurring_expenses:
                try:
                    expense_date = datetime(today.year, today.month, rec['day_of_month']).strftime('%Y-%m-%d')
                    add_expense(rec['name'], rec['category'], rec['amount'], expense_date, "Recurring Expense")
                except ValueError:
                    st.error(f"Could not add recurring expense '{rec['name']}' - Day {rec['day_of_month']} is not valid for this month.")
            st.success("Added all valid recurring expenses for this month!")


elif app_mode == "Set Category Budgets":
    st.header("Set Budgets for Categories")
    st.write("Define monthly spending limits for each category to stay on track.")
    
    category_budgets = get_category_budgets()
    
    with st.form("budget_form"):
        for category in EXPENSE_CATEGORIES:
            budget_val = st.number_input(f"Budget for {category} (₹)", 
                                         value=float(category_budgets.get(category, 0.0)),
                                         min_value=0.0,
                                         key=f"budget_{category}")
            set_category_budget(category, budget_val)
        
        if st.form_submit_button("Save Budgets"):
            st.success("Category budgets have been saved successfully!")
            st.rerun()
