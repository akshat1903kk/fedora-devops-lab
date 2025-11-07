import os
import pathlib

from dotenv import load_dotenv

# load .env from backend root
load_dotenv(pathlib.Path(__file__).resolve().parents[1] / ".env")

import app.models  # <-- IMPORTANT: imports your model modules so metadata is populated
from app.database import Base

target_metadata = Base.metadata
