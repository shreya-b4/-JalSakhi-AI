# JalSakhi AI — Village-friendly edition

## What is included
- Streamlit village-first interface with cream/green editorial styling inspired by the supplied reference recording.
- High-contrast text: light text on dark status panels; dark text on light cards.
- Resident navigation separated from VWSC/staff tools.
- Marathi/English issue labels and quick report flow.
- Household water-storage checklist.
- Downloadable report receipt.
- Five communicating agents: Communication, Testing, Alert, Escalation/Lab Coordination, and Village Record.
- Random Forest prototype model trained by `train_model.py`.

## Windows PowerShell setup (run one command at a time)
1. Extract this ZIP to Downloads.
2. Open PowerShell and run:

```powershell
cd "$HOME\Downloads\JalSakhi_Village_Easy"
```

If the extracted folder contains another `JalSakhi_AI` folder, run:

```powershell
cd "$HOME\Downloads\JalSakhi_Village_Easy\JalSakhi_AI"
```

If unsure, automatically locate `requirements.txt` from the extracted folder:

```powershell
$req = Get-ChildItem "$HOME\Downloads\JalSakhi_Village_Easy" -Filter requirements.txt -Recurse -File | Select-Object -First 1
if (-not $req) { throw "requirements.txt not found. Extract the ZIP again." }
Set-Location $req.DirectoryName
```

Then:

```powershell
py -3.11 -m venv .venv
```

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

```powershell
.\.venv\Scripts\python.exe train_model.py
```

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`.

## Important
- The training data and labels are synthetic prototype data. Reported validation accuracy is not real-world water-quality performance.
- The model is only a screening demonstration; it cannot certify drinking-water safety.
- The application stores demo records in Streamlit session state. They are not a shared database and may reset when the session ends.
- No real SMS, WhatsApp, government, laboratory, or sensor connection is included. Those require credentials, APIs, or physical data sources.
- Follow official local public-health guidance and verified laboratory/VWSC results.
