# Deploying to Streamlit Community Cloud

The easiest way to make this application public is to use [Streamlit Community Cloud](https://streamlit.io/cloud). It is free and connects directly to your GitHub repository.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account.
2.  **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/) using your GitHub account.

## Steps to Deploy

### 1. Push to GitHub

If you haven't already, push this code to a new GitHub repository.

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit of Vaccination Quality Guardian"

# Create a new repository on GitHub (https://github.com/new)
# Then link it here (replace URL with your repo URL):
git remote add origin https://github.com/YOUR_USERNAME/snowflake-vaccination-quality.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your repository (`snowflake-vaccination-quality`), branch (`main`), and main file path (`project.py`).
4.  Click **"Deploy!"**.

### 3. Done!

Streamlit will provision a server, install the dependencies from `requirements.txt`, and launch your app. You will get a public URL (e.g., `https://snowflake-vaccination-quality.streamlit.app`) that you can share with anyone.

---

## Alternative: Temporary Public URL (Local Tunnel)

If you just want to show someone quickly without deploying to GitHub, you can use `pyngrok`.

1.  Install pyngrok:
    ```bash
    pip install pyngrok
    ```
2.  Run Streamlit and create a tunnel:
    ```python
    # Create a file named run_public.py
    from pyngrok import ngrok
    import os

    # Start ngrok tunnel
    public_url = ngrok.connect(8501).public_url
    print(f"Public URL: {public_url}")

    # Run streamlit
    os.system("streamlit run project.py")
    ```
