from platform import processor
from .. import models, schemas
from fastapi import  File, HTTPException, UploadFile, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from ..core import logique
from typing import List


router =  APIRouter(prefix="/summaries", tags=["Summaries"])


processor = logique.LexiProcessor()

# Create
@router.post("/summarize_url", response_model= schemas.SummaryRead)
def summarize_url(url: schemas.URL, 
				  db: Session = Depends(get_db), 
				  current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""
	Résume le contenu d'une URL et enregistre dans la DB.
	"""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

	try:
		payload = processor.process_from_url(url.url)  # renvoie un schemas.SummaryCreate
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

	data = payload.dict() if hasattr(payload, "dict") else dict(payload)
	data["owner_id"] = current_user.id
	new_summary = models.Summary(**data)
	db.add(new_summary)
	db.commit()
	db.refresh(new_summary)

	return new_summary


@router.post("/summarize_pdf", response_model=schemas.SummaryRead)
def summarize_pdf(file: UploadFile = File(...), 
				  db: Session = Depends(get_db), 
				  current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""
	Résume le contenu d'un PDF uploadé et enregistre dans la DB.
	"""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

	# Sauvegarde temporaire du fichier
	import os
	import shutil
	import tempfile
	suffix = ".pdf"
	tmp_path = None
	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
			shutil.copyfileobj(file.file, tmp)
			tmp_path = tmp.name

		payload = processor.process_from_pdf(tmp_path)

		if isinstance(payload, dict) and "error" in payload:
			raise HTTPException(status_code=400, detail=payload["error"])

		data = payload.dict() if hasattr(payload, "dict") else dict(payload)
		data["owner_id"] = current_user.id
		new_summary = models.Summary(**data)
		db.add(new_summary)
		db.commit()
		db.refresh(new_summary)
		return new_summary
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	finally:
		try:
			if tmp_path and os.path.exists(tmp_path):
				os.remove(tmp_path)
		except Exception:
			pass


@router.post("/summarize_pdf_url", response_model=schemas.SummaryRead)
def summarize_pdf_url(pdf_url: schemas.URL, 
					  db: Session = Depends(get_db), 
					  current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	
	"""Télécharge un PDF depuis une URL, le résume et enregistre dans la DB."""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

	import os
	import tempfile
	try:
		import requests
		response = requests.get(pdf_url.url, timeout=10)
		response.raise_for_status()
	except Exception as e:
		raise HTTPException(status_code=400, detail=f"Impossible de télécharger le PDF : {e}")

	suffix = ".pdf"
	tmp_path = None
	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
			tmp.write(response.content)
			tmp_path = tmp.name

		payload = processor.process_from_pdf(tmp_path)

		if isinstance(payload, dict) and "error" in payload:
			raise HTTPException(status_code=400, detail=payload["error"])

		data = payload.dict() if hasattr(payload, "dict") else dict(payload)
		data["owner_id"] = current_user.id
		new_summary = models.Summary(**data)
		db.add(new_summary)
		db.commit()
		db.refresh(new_summary)
		return new_summary
	finally:
		try:
			if tmp_path and os.path.exists(tmp_path):
				os.remove(tmp_path)
		except Exception:
			pass

###GET
####Read 
@router.get("/", response_model=List[schemas.SummaryRead])
def get_all_summaries(db: Session = Depends(get_db), 
					  current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	
	"""
	Récupère tous les résumés.
	"""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
	
	return db.query(models.Summary).filter(models.Summary.owner_id == current_user.id).all()

# get a summary by id
@router.get("/{summary_id}", response_model=schemas.SummaryRead)
def get_summary(summary_id: int, 
				db: Session = Depends(get_db), 
				current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""
	Récupère un résumé par son ID.
	"""

	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
	
	summary = db.query(models.Summary).filter(models.Summary.id == summary_id).first()
	if not summary:
		raise HTTPException(status_code=404, detail="Résumé non trouvé")
	if getattr(summary, "owner_id", None) not in (None, current_user.id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
	return summary


# get a summary by a name, the name must be in the database
@router.get("/summary/name/{name}", response_model=schemas.SummaryRead)
def get_summary_by_name(name: str, 
						db: Session = Depends(get_db), 
						current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""Récupère un résumé par son nom."""

	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

	summary = db.query(models.Summary).filter(models.Summary.title == name).first()
	all_titles = db.query(models.Summary.title).all()
	if not summary:
		raise HTTPException(status_code=404, detail=f"Résumé non trouvé.\n Voici la liste des titres disponibles : {[title for (title,) in all_titles]}")
	if getattr(summary, "owner_id", None) not in (None, current_user.id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
	return summary


####DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(id:int, 
				   db: Session=Depends(get_db), 
				   current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""Supprime un résumé par son ID."""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")


	summary_query = db.query(models.Summary).filter(models.Summary.id == id)
	summary_delete = summary_query.first()
	if not summary_delete:
		raise HTTPException(detail="This summary does not exist.", status_code=404)
	if getattr(summary_delete, "owner_id", None) not in (None, current_user.id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
	
	summary_query.delete(synchronize_session=False)
	db.commit()

# delete the summary by its name
@router.delete("/summary/name/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary_by_name(name: str, 
							db: Session = Depends(get_db), 
							current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
	"""Supprime un résumé par son nom."""
	if not current_user:
		raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

	summary_query = db.query(models.Summary).filter(models.Summary.title == name)
	summary_delete = summary_query.first()
	if not summary_delete:
		raise HTTPException(detail="This summary does not exist.", status_code=404)
	if getattr(summary_delete, "owner_id", None) not in (None, current_user.id):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

	summary_query.delete(synchronize_session=False)
	db.commit()

