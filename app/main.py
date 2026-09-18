import sys
import os
import subprocess
import threading
import time
import uvicorn
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()


def run_backend():
    try:
        logger.info("Starting backend service (FastAPI on http://127.0.0.1:8000)...")
        uvicorn.run("app.backend.api:app", host="127.0.0.1", port=8000, reload=False)
    except Exception as e:
        logger.error(f"Failed to start backend service: {CustomException('Error starting backend service', e)}")


def run_frontend():
    try:
        logger.info("Starting frontend service (Streamlit on http://127.0.0.1:8501)...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/frontend/ui.py", "--server.port", "8501"])
    except Exception as e:
        logger.error(f"Failed to start frontend service: {CustomException('Error starting frontend service', e)}")


if __name__ == "__main__":
    try:
        logger.info("Starting both frontend and backend services...")
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        frontend_thread = threading.Thread(target=run_frontend, daemon=True)

        backend_thread.start()
        time.sleep(2)
        frontend_thread.start()

        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down Multi-AI Agent services...")
    except Exception as e:
        logger.error(f"Failed to start services: {CustomException('Error starting services', e)}")