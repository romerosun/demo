# Labor Standards Story

A fixed, top-to-bottom Streamlit visual story explaining why generic PPH is not a labor standard, how MOST makes work measurable, and how a digital twin supports better labor, flow, and layout decisions.

The app intentionally contains no visitor controls, financial claims, or client results.

## Included

- Hero warehouse digital-twin visual
- Short-route versus complex-route pallet infographic
- MOST to standard library to workload forecast visual flow
- Digital-twin scenarios for labor, work, and layout

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
