# app/main.py
import tempfile
from typing import List
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..app.core import logique
from .database import get_db, engine
from . import schemas
from . import models


models.Base.metadata.create_all(bind=engine) # crée la table dans la base si elle n'existe pas sinon elle va juste la loader

app = FastAPI(title="LexiTrack API")



