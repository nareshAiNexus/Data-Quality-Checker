
### 1. Problem Statement
Build a Gen AI agent that can analyze a CSV file and generate a natural language report
about the file’s data quality issues — like missing values, duplicate rows, outliers, wrong datatypes, etc.

### 2. Why It Matters
In real-world projects, bad data = bad analytics.
Data engineers usually write manual scripts to check quality.
With this project, an LLM will automate the boring initial analysis.

### 3. Architecture Diagram
User Uploads CSV
      ↓
Python (streamlit Backend) Reads File
      ↓
Summarizes data stats (like missing %, outliers) using Pandas
      ↓
LLM (local or OpenAI) Generates a human-readable Data Quality Report
      ↓
Returns the Report to User

### 4. Tech Stack

- Item                    Tool
- Backend             Python + Streamlit
- Data Processing     Pandas
- LLM                 deepseek r0528:free
- Frontend            streamlit
