📈 Technical Chart with Search Bar
Live App: https://technical-chart-with-search-bar-5uvvtdbazuyzxdq6fdtppt.streamlit.app/

GitHub Repository: https://github.com/SureshPatel9765/Technical-Chart-With-Search-Bar

🧭 Overview
This Streamlit application allows users to visualize technical charts for NSE stocks. Users can input stock symbols via a text box, select from a dropdown of popular stocks, or use an autocomplete search bar. The application fetches data through Google Finance, ensuring real-time updates without IP blocking concerns.

🚀 Features

Multiple Input Methods:

Text Input: Manually enter any valid NSE stock symbols.

Dropdown Selection: Choose from a list of popular NSE stocks.

Autocomplete Search Bar: Search and select stocks with real-time suggestions.

Interactive Chart Display:

Price Chart: Visualize stock closing prices.

RSI Chart: View the Relative Strength Index.

Toggle Options: Use radio buttons to switch between chart types or view both simultaneously.

State Management:

Seamless toggling between input methods.

Automatic clearing of previous inputs to prevent conflicts.

Data Retrieval:

Fetches stock data using the GOOGLEFINANCE function in Google Sheets.

Eliminates the risk of IP blocking associated with direct API calls.

🛠️ Installation & Setup
Clone the Repository:


git clone https://github.com/SureshPatel9765/Technical-Chart-With-Search-Bar.git
cd Technical-Chart-With-Search-Bar
Install Dependencies:


pip install -r requirements.txt
Configure Google Sheets Access:

Create a Google Cloud project and enable the Google Sheets API.

Generate a service account and download the credentials JSON file.

Save the credentials as secrets.toml in the .streamlit directory:
toml

[gcp_service_account]
type = "service_account"
project_id = "your_project_id"
private_key_id = "your_private_key_id"
private_key = "your_private_key"
client_email = "your_client_email"
client_id = "your_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your_client_x509_cert_url"


streamlit run appsearch.py
📂 File Structure
sql
Copy code
Technical-Chart-With-Search-Bar/
├── appsearch.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
🔐 Secrets Management
Local Development:

Store your Google service account credentials in .streamlit/secrets.toml.

Streamlit Cloud Deployment:

Navigate to your app's dashboard.

Click on Settings > Secrets.

Paste your credentials in the provided editor.

⚠️ Notes
Search Box Clearing:

Due to limitations with the streamlit-searchbox component, the search input may not clear programmatically when switching input methods. Users can manually clear the input using the provided 'X' icon.

Shared Google Sheet:

If multiple apps access the same Google Sheet, ensure they operate on separate worksheets or implement appropriate data handling to prevent conflicts.

📄 License
This project is public and not under any license.
 






