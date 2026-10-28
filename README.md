# Data-Driven Decisions

A fixed, top-to-bottom Streamlit introduction to a distribution-center digital twin. It shows how a model can make labor, flow, bottlenecks, delays, and operating decisions visible.

The app intentionally contains no visitor controls, financial claims, or client results.

## Included

- Simio-style warehouse hero visual
- Simple map → model → validate explanation
- Clean operational dashboard illustration with heat, delay, and labor-balance views
- Practical action areas: scheduling, scaling, and cost comparison

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

1. Refine the warehouse visual and process language for the target sector.
2. Add a real anonymized case study only after the numbers are validated.
3. Add a contact section and professional background.
