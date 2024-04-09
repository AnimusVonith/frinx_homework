# PostgreSQL Data Insertion Program

This Python script reads data from a JSON file and inserts the extracted information into a PostgreSQL database table.

## Usage

1. **Setup:**
   - Install Python 3.6+ and PostgreSQL 10+.
   - Create a PostgreSQL database.
   - Create a table named `frinx_configs` with the following structure:
     ```sql
     CREATE TABLE frinx_configs (
         id SERIAL PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         description VARCHAR(255),
         max_frame_size INTEGER,
         config JSON,
         port_channel_id INTEGER
     );
     ```

2. **Installation:**
   - Install required Python libraries:
     ```
     pip install -r requirements.txt
     ```

3. **Execution:**
   - Before running the script, set the following environment variables:
     - `DATABASE_NAME`: Name of the PostgreSQL database
     - `DATABASE_USER`: Username for PostgreSQL
     - `DATABASE_PASS`: Password for PostgreSQL
     - `DATABASE_HOST`: Host address of the PostgreSQL server
     - `DATABASE_PORT`: Port number for PostgreSQL (default: 5432)

   - Prepare your JSON data file (`configClear_v2.json`).
   - Run the script:
     ```
     python insert_data.py
     ```

4. **Batch Script:**
   - Alternatively, use `template_run.bat` to set environment variables and run the script.
     ```
     template_run.bat
     ```
