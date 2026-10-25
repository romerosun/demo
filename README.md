# Labor Standards + Simulation Case Study

An interactive Streamlit portfolio case study showing why generic pallets-per-hour planning can misstate labor demand, and how labor standards, workload forecasting, and simulation improve decisions.

All values in the app are assumptions for demonstration purposes. They are not client results.

## Included

- Interactive 3D warehouse layouts for current and redesigned operations
- Generic PPH versus task-hours workload chart
- Editable financial, staffing, and improvement assumptions
- Before/after cost tables and scenario comparison
- Explanation of the MOST to forecast to simulation workflow

## Run locally

Windows PowerShell:

~~~
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
~~~

macOS or Linux:

~~~
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
~~~

## Deploy from GitHub to Streamlit Community Cloud

1. Create a new GitHub repository, for example labor-standards-simulator.
2. Upload this folder's contents, including app.py and requirements.txt, to the repository root.
3. In Streamlit Community Cloud, choose Create app.
4. Choose the repository and branch.
5. Set the main file path to app.py.
6. Deploy.

## Next improvements

1. Replace illustrative assumptions with a sharper agreed business case.
2. Refine the 3D warehouse to resemble the target sector.
3. Add actual scenario output from Simio or a Python model.
4. Add a contact section and professional background.
