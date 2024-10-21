
# **ImportXport**  

**ImportXport** is a Django-based project that enables seamless import and export of data from and to CSV files using custom Django commands. This tool is perfect for data migration, backup, and synchronization between systems.

## **Features**  
- Export model data from the database to a CSV file with a timestamped filename.
- Import data from a CSV file into a specified model.
- Handles duplicate record checks during import.
- Provides helpful error messages for missing models and records.

---

## **How to Use**

### **Setup Instructions**  
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/ImportXport.git
   cd ImportXport
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**  
   ```bash
   python manage.py createsuperuser
   ```

---

### **Usage Instructions**

#### **Export Data to CSV**  
Use the following command to export data from a model to a CSV file:

```bash
python manage.py exportdata modelname
```

- **Example:**
   ```bash
   python manage.py exportdata Student
   ```

- The data will be saved in a file named like:
  ```
  exported_Student_data_21-10-2024-15-30.csv
  ```

#### **Import Data from CSV**  
Use the following command to import data into a specific model:

```bash
python manage.py importdata path/to/your_file.csv modelname
```

- **Example:**
   ```bash
   python manage.py importdata data/students.csv Student
   ```

- If a record with the same **roll_number** exists, it will skip that entry with an error message.

---

## **Code Explanation**

### **Export Command**:  
Located in `your_app/management/commands/exportdata.py`.

This command:
- Searches for the specified model in all Django apps.
- Exports all records from the model to a timestamped CSV file.
- Handles exceptions like missing models or empty data.

```python
python manage.py exportdata Student
```

---

### **Import Command**:  
Located in `your_app/management/commands/importdata.py`.

This command:
- Reads data from a CSV file.
- Searches for the specified model.
- Checks for duplicate records using the **roll_number** field.
- Inserts data into the database if it passes the checks.

```python
python manage.py importdata students.csv Student
```

---

## **Project Structure**
```
ImportXport/
│
├── your_app/
│   ├── management/
│   │   └── commands/
│   │       ├── exportdata.py
│   │       └── importdata.py
│
├── requirements.txt
└── README.md
```

---

## **Possible Errors & Handling**
- **Model not found:**  
   ```bash
   Model Student not Found in any app
   ```
- **Duplicate record:**  
   ```bash
   student with this roll_number already exists
   ```
- **File not found:**  
   ```bash
   [Errno 2] No such file or directory: 'students.csv'
   ```

---

## **Contributing**  
Feel free to fork the repository and submit pull requests with improvements or new features!

---

## **License**  
This project is licensed under the MIT License.


