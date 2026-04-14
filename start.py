import subprocess
import sys

from pyngrok import ngrok

share = "--share" in sys.argv

if share:
    tunnel = ngrok.connect(8501)
    print(f"\nLive at: {tunnel.public_url}\n")

subprocess.run(["streamlit", "run", "app.py"])
