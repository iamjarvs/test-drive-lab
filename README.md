# Apstra Lab Hub

This repository now serves a small Streamlit website with:

- A read-only lab table shown at the top of the page
- Link cards for the lab guide, DCA sign-up, and other resources
- A basic password-protected CSV upload flow for replacing the lab table

## 1. Install dependencies

From the repository directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Update hardcoded links and password

The app uses top-level constants in [test_drive_page.py](test_drive_page.py) for the published links and upload password.

Update these values near the top of the file:

```python
ADMIN_PASSWORD = "C1sco123!"
LAB_GUIDE_URL = "https://example.com/lab-guide"
DCA_SIGNUP_URL = "https://dc.ai.juniper.net/"
APSTRA_UI_URL = "https://example.com/apstra-ui"
OPS_NOTES_URL = "https://example.com/operations"
```

## 3. Run on a specific port

Example using port 8080:

```bash
streamlit run test_drive_page.py --server.address 0.0.0.0 --server.port 8080
```

For server use, you can now restart the app with one command:

```bash
./run_server.sh
```

That script:

- Kills any existing Streamlit process for this app
- Kills anything still listening on port 8080
- Restarts the app in the background
- Writes logs to `logs/streamlit.log`

You can also override the port when starting it:

```bash
PORT=8080 ./run_server.sh
```

Open:

```text
http://localhost:8080
```

If this needs to be reachable from other machines, open the same port on the host firewall and browse to:

```text
http://YOUR_HOSTNAME_OR_IP:8080
```

## 4. Update the lab table

1. Open the site.
2. Click Admin: Update Lab Details at the bottom of the page.
3. Enter the upload password from [test_drive_page.py](test_drive_page.py).
4. Upload a UTF-8 CSV file.
5. Click Replace Lab Table.

The uploaded CSV replaces data/qq-users.csv and the page refreshes with the new data.

## 5. CSV format

The uploader accepts any UTF-8 CSV file with:

- A header row
- At least one data row

The sample file is data/qq-users.csv.

## 6. HTTP and HTTPS behavior

This app runs over HTTP by default.

Important limitation: a browser cannot reliably fall back from https://... to http://... unless you have something listening on the HTTPS port first. That means:

- If a user types an HTTPS URL and nothing is serving TLS on that port, the request fails before Streamlit can redirect.
- If you want automatic HTTPS-to-HTTP redirection, you need a reverse proxy on port 443 with a certificate.

Practical options:

1. Publish the exact HTTP URL and keep the site HTTP-only.
2. Put Nginx or Caddy in front of Streamlit and either redirect HTTPS to HTTP or, preferably, serve proper HTTPS.

In most cases, serving proper HTTPS is the better deployment choice.