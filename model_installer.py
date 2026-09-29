from pathlib import Path
import urllib.request

URL = "https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/resolve/main/LFM2.5-1.2B-Instruct-Q4_K_M.gguf"

OUTPUT = Path("models/lfm2.5/LFM2.5-1.2B-Instruct-Q4_K_M.gguf")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

print("Downloading LFM2.5...")

urllib.request.urlretrieve(URL, OUTPUT)

print(f"Downloaded to: {OUTPUT}")