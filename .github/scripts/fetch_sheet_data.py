name: Fetch Google Sheets Data

on:
  schedule:
    - cron: '0 0 * * *'  # Runs every day at midnight
  workflow_dispatch:  # Allows manual triggering

jobs:
  fetch-sheet-data:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

    - name: Fetch Google Sheets data
      env:
        GOOGLE_SHEETS_CREDENTIALS: ${{ secrets.GOOGLE_SHEETS_CREDENTIALS }}
      run: |
        python .github/scripts/fetch_sheet_data.py

    - name: Commit and push if changed
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add -A
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update data from Google Sheets" && git push)
