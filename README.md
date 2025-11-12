Data Quality & Validation Framework
A simple and interactive tool that checks the quality of any CSV dataset.

It helps you quickly find problems like:
Missing values
Wrong data types
Outliers (unusual values)
Schema mismatches
This project is useful for anyone working with data pipelines or preparing data for analysis or machine learning.

🚀 Why I Built This
In real data engineering work, data is often messy.
Before loading it into a database or using it for analysis, you must check its quality.
This tool makes that step easy and visual.
You upload a CSV, click one button, and instantly see where the data has issues.

🧰 Tech Stack
Python
Pandas (data processing)
NumPy
SciPy (z-score outlier detection)
Streamlit (UI)
Slack SDK (optional alerts)
dotenv (environment variables)

📂 Project Structure
data_quality_framework/
│
├── data/
│     └── sample_data.csv
│
├── src/
│     ├── __init__.py
│     ├── validator.py
│     ├── notifier.py
│     ├── data_generator.py
│     └── streamlit_app.py
│
└── requirements.txt

▶️ How to Run the App
1. Install all requirements
pip install -r requirements.txt

2. Generate sample test data
python src/data_generator.py

3. Start the Streamlit app
streamlit run src/streamlit_app.py

4. Use the App
Upload your own CSV OR
Use the default /data/sample_data.csv
Adjust thresholds
Click Run Validation

You will see a summary showing:
Null percentages
Outlier counts
Schema checks
Total rows