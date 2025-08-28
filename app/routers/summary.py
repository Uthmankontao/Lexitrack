from platform import processor
from .. import models, schemas, utils
from fastapi import Body, FastAPI, File, HTTPException, Response, UploadFile, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from typing import List, Optional
from sqlalchemy import func
from ..core import logique

import tempfile

import app

router =  APIRouter(prefix="/summaries", tags=["Summaries"])


processor = logique.LexiProcessor()

###POST
#### Create
@router.post("/summarize_url", response_model= schemas.SummaryRead)
def summarize_url(url: schemas.URL, db: Session = Depends(get_db)):
    """
    Résume le contenu d'une URL et enregistre dans la DB.
    """
    try:
        payload = processor.process_from_url(url.url)  # renvoie un schemas.SummaryCreate
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_summary = models.Summary(**payload.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    return new_summary


@router.post("/summarize_pdf", response_model=schemas.SummaryRead)
def summarize_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Résume le contenu d'un PDF uploadé et enregistre dans la DB.
    """
    # Sauvegarde temporaire du fichier
    import shutil
    import tempfile
    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    payload = processor.process_from_pdf(tmp_path, db_session=db)

    # Supprimer le fichier temporaire
    import os
    os.remove(tmp_path)

    new_summary = models.Summary(**payload.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    if isinstance(new_summary, dict) and "error" in new_summary:
        raise HTTPException(status_code=400, detail=new_summary["error"])
    return new_summary

@router.post("/summarize_pdf_url", response_model=schemas.SummaryRead)
def summarize_pdf_url(pdf_url: schemas.URL, db: Session = Depends(get_db)):
    """Télécharge un PDF depuis une URL, le résume et enregistre dans la DB."""
    try:
        import requests
        import os
        response = requests.get(pdf_url.url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Impossible de télécharger le PDF : {e}")

    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    payload = processor.process_from_pdf(tmp_path, db_session=db)

    os.remove(tmp_path)

    new_summary = models.Summary(**payload.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    if isinstance(new_summary, dict) and "error" in new_summary:
        raise HTTPException(status_code=400, detail=new_summary["error"])
    return new_summary

###GET
####Read 
@app.get("/", response_model=List[schemas.SummaryRead])
def get_all_summaries(db: Session = Depends(get_db)):
    return db.query(models.Summary).all()

# get a summary by id
@app.get("/{summary_id}", response_model=schemas.SummaryRead)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(models.Summary).filter(models.Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Résumé non trouvé")
    return summary


# get a summary by a name, the name must be in the database
@app.get("/summary/name/{name}", response_model=schemas.SummaryRead)
def get_summary_by_name(name: str, db: Session = Depends(get_db)):
    summary = db.query(models.Summary).filter(models.Summary.title == name).first()
    all_titles = db.query(models.Summary.title).all()
    if not summary:
        raise HTTPException(status_code=404, detail=f"Résumé non trouvé.\n Voici la liste des titres disponibles : {[title for (title,) in all_titles]}")
    return summary


####DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(id:str, db: Session=Depends(get_db)):
    summary_query = db.query(models.Summary).filter(models.Summary.id == id)
    summary_delete = summary_query.first()
    if not summary_delete:
        raise HTTPException(detail="This summary does not exist.", status_code=404)
    
    summary_query.delete(synchronize_session=False)
    db.commit()
