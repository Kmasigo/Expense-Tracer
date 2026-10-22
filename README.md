# Expense Tracer

A simple Flet web app for recording expenses in South African rand (R), assigning categories, viewing the total, and deleting entries.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python main.py`.

## Publish a public link with Render

This repository includes `render.yaml` for Render's Blueprint deployment.

1. Sign in to GitHub and create a **new public repository** named `expense-tracer`.
2. Upload `main.py`, `models.py`, `requirements.txt`, `render.yaml`, and this README to the repository root.
3. Sign in to Render and choose **New + → Blueprint**.
4. Connect the GitHub repository and deploy the `expense-tracer` service.
5. When deployment finishes, Render will show a public URL similar to `https://expense-tracer-xxxx.onrender.com`. Copy that URL and share it.

You need to complete the GitHub/Render account authorization yourself; this package does not create a live hosted URL on its own.

## Important storage note

Expenses are stored in `data/expenses.json` on the server. On free hosting, local files can be erased when the service restarts or redeploys. This is suitable for a demo, but not reliable long-term storage for real users. For persistent records, connect a database or a persistent disk.
