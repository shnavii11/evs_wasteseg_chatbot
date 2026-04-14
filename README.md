# WasteWise ♻️

A local AI chatbot that tells you how to dispose of any waste item responsibly — built for Mumbai/Maharashtra residents. Powered by Ollama (llama3.1:8b), runs fully offline.

Built as part of an EVS project on residential waste recycling behaviour (survey n=52).

---

## Prerequisites

- [Ollama](https://ollama.com/download) installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- `llama3.1:8b` model pulled — run `ollama pull llama3.1:8b` once

---

## Setup

```bash
git clone https://github.com/gg21-prog/evs_wasteseg_chatbot.git
cd evs_wasteseg_chatbot
uv sync
```

---

## Launch

Open **two terminals**:

**Terminal 1**
```bash
ollama serve
```

**Terminal 2**
```bash
cd evs_wasteseg_chatbot
source .venv/bin/activate
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Share a public link (optional)

If you want to share the chatbot with someone via a live link, set up [ngrok](https://ngrok.com) and run this instead in Terminal 2:

```bash
cd evs_wasteseg_chatbot
source .venv/bin/activate
python -c "
from pyngrok import ngrok
import subprocess
tunnel = ngrok.connect(8501)
print('Live at:', tunnel.public_url)
subprocess.run(['streamlit', 'run', 'app.py'])
"
```

The printed URL can be opened by anyone while your terminal is running.
