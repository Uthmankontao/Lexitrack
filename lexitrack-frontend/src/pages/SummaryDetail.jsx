import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import './SummaryDetail.css';

function SummaryDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  // Get token from localStorage
  const getToken = () => {
    return localStorage.getItem("token");
  };

  // Fetch summary details
  const fetchSummaryDetail = async () => {
    const token = getToken();
    if (!token) {
      setError("Vous devez être connecté");
      setIsLoading(false);
      setTimeout(() => navigate("/login"), 2000);
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/summaries/${id}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSummary(data);
        setError("");
      } else if (response.status === 401) {
        setError("Session expirée, veuillez vous reconnecter");
        setTimeout(() => navigate("/login"), 2000);
      } else if (response.status === 404) {
        setError("Résumé non trouvé");
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Erreur lors du chargement");
      }
    } catch (err) {
      setError("Impossible de joindre le serveur");
      console.error("Erreur lors du chargement du résumé:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSummaryDetail();
  }, [id]);

  const handleGoBack = () => {
    navigate("/dashboard");
  };

  const handleDelete = async () => {
    const token = getToken();
    if (!token) return;

    if (!window.confirm("Êtes-vous sûr de vouloir supprimer ce résumé ?")) return;

    try {
      const response = await fetch(`http://127.0.0.1:8000/summaries/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (response.status === 204) {
        navigate("/dashboard");
      } else {
        const errorData = await response.json();
        alert("Erreur : " + errorData.detail);
      }
    } catch {
      alert("Erreur : Impossible de supprimer le résumé");
    }
  };

  if (isLoading) {
    return (
      <div className="detail-container loading-container">
        <div className="spinner-large"></div>
        <p>Chargement du résumé...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="detail-container error-container">
        <div className="error-icon">⚠️</div>
        <h2>Une erreur est survenue</h2>
        <p>{error}</p>
        <button onClick={handleGoBack} className="btn-back">
          Retour au Dashboard
        </button>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="detail-container error-container">
        <div className="error-icon">📭</div>
        <h2>Résumé introuvable</h2>
        <button onClick={handleGoBack} className="btn-back">
          Retour au Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="detail-container">
      {/* Header with back button */}
      <header className="detail-header">
        <button onClick={handleGoBack} className="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          <span>Retour</span>
        </button>
        <button onClick={handleDelete} className="delete-button">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
          <span>Supprimer</span>
        </button>
      </header>

      {/* Main content */}
      <div className="detail-content">
        <div className="detail-card">
          {/* Title section */}
          <div className="title-section">
            <div className="title-icon">📄</div>
            <h1>{summary.title || "Sans titre"}</h1>
          </div>

          {/* Metadata */}
          <div className="metadata-section">
            <div className="metadata-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <span>
                {summary.created_at
                  ? new Date(summary.created_at).toLocaleDateString("fr-FR", {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })
                  : "Date inconnue"}
              </span>
            </div>
            {summary.source_url && (
              <a 
                href={summary.source_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="metadata-link"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
                <span>Voir la source</span>
              </a>
            )}
          </div>

          {/* Summaries content */}
          {summary.summary && (
            <div className="summaries-container">
              {/* Short summary */}
              {summary.summary.short && (
                <div className="summary-section short-summary">
                  <div className="section-header">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 20h9"/>
                      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
                    </svg>
                    <h2>Résumé court</h2>
                  </div>
                  <div className="section-content">
                    <p>{summary.summary.short}</p>
                  </div>
                </div>
              )}

              {/* Detailed summary */}
              {summary.summary.detailed && (
                <div className="summary-section detailed-summary">
                  <div className="section-header">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                      <polyline points="10 9 9 9 8 9"/>
                    </svg>
                    <h2>Résumé détaillé</h2>
                  </div>
                  <div className="section-content">
                    <p>{summary.summary.detailed}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* If no summary content */}
          {!summary.summary && (
            <div className="no-content">
              <p>Aucun contenu de résumé disponible</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SummaryDetail;