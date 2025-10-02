import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import './Dashboard.css';

function Dashboard() {
  const [activeTab, setActiveTab] = useState("list");
  const [summaries, setSummaries] = useState([]);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  // Form states
  const [url, setUrl] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [searchName, setSearchName] = useState("");

  const navigate = useNavigate();

  // Get token from localStorage
  const getToken = () => {
    return localStorage.getItem("token");
  };

  // Fetch all summaries
  const fetchSummaries = async () => {
    const token = getToken();
    if (!token) {
      setMessage("Erreur : Vous devez être connecté");
      setMessageType("error");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/summaries/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSummaries(data);
        setMessage("");
      } else if (response.status === 401) {
        setMessage("Erreur : Session expirée, veuillez vous reconnecter");
        setMessageType("error");
        setTimeout(() => navigate("/login"), 2000);
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch (err) {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
      console.error("Erreur lors du chargement des résumés:", err);
    }
  };

  // Summarize from URL
  const handleSummarizeUrl = async (e) => {
    e.preventDefault();
    const token = getToken();
    if (!token) return;

    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/summaries/summarize_url", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      });

      if (response.ok) {
        setMessage("Résumé créé avec succès !");
        setMessageType("success");
        setUrl("");
        setTimeout(() => {
          fetchSummaries();
          setActiveTab("list");
        }, 500);
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch (err) {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
      console.error("Erreur lors de la création du résumé:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Summarize from PDF file
  const handleSummarizePdf = async (e) => {
    e.preventDefault();
    const token = getToken();
    if (!token || !pdfFile) return;

    setIsLoading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", pdfFile);

      const response = await fetch("http://127.0.0.1:8000/summaries/summarize_pdf", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        setMessage("Résumé du PDF créé avec succès !");
        setMessageType("success");
        setPdfFile(null);
        document.getElementById("pdf-file-input").value = "";
        setTimeout(() => {
          fetchSummaries();
          setActiveTab("list");
        }, 500);
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch (err) {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
      console.error("Erreur lors de la création du résumé PDF:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Summarize from PDF URL
  const handleSummarizePdfUrl = async (e) => {
    e.preventDefault();
    const token = getToken();
    if (!token) return;

    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/summaries/summarize_pdf_url", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: pdfUrl })
      });

      if (response.ok) {
        setMessage("Résumé du PDF créé avec succès !");
        setMessageType("success");
        setPdfUrl("");
        setTimeout(() => {
          fetchSummaries();
          setActiveTab("list");
        }, 500);
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch (err) {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
      console.error("Erreur lors de la création du résumé PDF URL:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Delete summary by ID
  const handleDelete = async (id) => {
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
        setMessage("Résumé supprimé avec succès");
        setMessageType("success");
        fetchSummaries();
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
    }
  };

  // Search summary by name
  const handleSearchByName = async (e) => {
    e.preventDefault();
    const token = getToken();
    if (!token) return;

    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch(`http://127.0.0.1:8000/summaries/summary/name/${encodeURIComponent(searchName)}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSummaries([data]);
        setMessage("Résumé trouvé !");
        setMessageType("success");
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
    } finally {
      setIsLoading(false);
    }
  };

  // Navigate to summary detail
  const handleViewDetail = (id) => {
    navigate(`/summary/${id}`);
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  // Load summaries on mount
  useEffect(() => {
    fetchSummaries();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>LexiTrack Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Déconnexion</button>
      </header>

      <div className="dashboard-content">
        {/* Navigation Tabs */}
        <nav className="tabs">
          <button 
            className={activeTab === "list" ? "tab active" : "tab"}
            onClick={() => setActiveTab("list")}
          >
            Mes Résumés
          </button>
          <button 
            className={activeTab === "url" ? "tab active" : "tab"}
            onClick={() => setActiveTab("url")}
          >
            Résumer URL
          </button>
          <button 
            className={activeTab === "pdf" ? "tab active" : "tab"}
            onClick={() => setActiveTab("pdf")}
          >
            Résumer PDF
          </button>
          <button 
            className={activeTab === "pdf-url" ? "tab active" : "tab"}
            onClick={() => setActiveTab("pdf-url")}
          >
            Résumer PDF (URL)
          </button>
        </nav>

        {/* Message Display */}
        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}

        {/* Tab Content */}
        <div className="tab-content">
          {/* List Summaries */}
          {activeTab === "list" && (
            <div className="summaries-section">
              <div className="search-bar">
                <form onSubmit={handleSearchByName}>
                  <input
                    type="text"
                    placeholder="Rechercher par nom..."
                    value={searchName}
                    onChange={(e) => setSearchName(e.target.value)}
                  />
                  <button type="submit" disabled={isLoading}>Rechercher</button>
                  <button type="button" onClick={fetchSummaries}>Tout afficher</button>
                </form>
              </div>

              {summaries.length === 0 ? (
                <div className="empty-state">
                  <p>Aucun résumé pour le moment</p>
                  <p className="hint">Créez votre premier résumé en utilisant les onglets ci-dessus</p>
                </div>
              ) : (
                <div className="summaries-grid">
                  {summaries.map((summary) => (
                    <div key={summary.id} className="summary-card">
                      <div className="summary-header">
                        <h3>{summary.title || "Sans titre"}</h3>
                        <button 
                          onClick={() => handleDelete(summary.id)}
                          className="delete-btn"
                          title="Supprimer"
                        >
                          ✕
                        </button>
                      </div>

                      {/* Affichage des résumés selon le schéma Pydantic */}
                      <div className="summary-content">
                        {summary.summary && (
                          <>
                            {summary.summary.short && (
                              <p className="summary-preview">
                                <strong>Résumé court :</strong> {
                                  summary.summary.short.length > 150 
                                    ? summary.summary.short.substring(0, 150) + "..." 
                                    : summary.summary.short
                                }
                              </p>
                            )}
                            {summary.summary.detailed && (
                              <p className="summary-preview">
                                <strong>Résumé détaillé :</strong> {
                                  summary.summary.detailed.length > 200 
                                    ? summary.summary.detailed.substring(0, 200) + "..." 
                                    : summary.summary.detailed
                                }
                              </p>
                            )}
                          </>
                        )}
                      </div>

                      <div className="summary-footer">
                        <span className="summary-date">
                          {summary.created_at
                            ? new Date(summary.created_at).toLocaleDateString("fr-FR")
                            : "Date inconnue"}
                        </span>
                        <button 
                          onClick={() => handleViewDetail(summary.id)}
                          className="view-btn"
                        >
                          Voir plus
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Summarize URL */}
          {activeTab === "url" && (
            <div className="form-section">
              <h2>Résumer une page web</h2>
              <form onSubmit={handleSummarizeUrl}>
                <div className="form-group">
                  <label>URL de la page</label>
                  <input
                    type="url"
                    placeholder="https://example.com/article"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" disabled={isLoading}>
                  {isLoading ? "Traitement en cours..." : "Créer le résumé"}
                </button>
              </form>
            </div>
          )}

          {/* Summarize PDF */}
          {activeTab === "pdf" && (
            <div className="form-section">
              <h2>Résumer un fichier PDF</h2>
              <form onSubmit={handleSummarizePdf}>
                <div className="form-group">
                  <label>Fichier PDF</label>
                  <input
                    id="pdf-file-input"
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setPdfFile(e.target.files[0])}
                    required
                  />
                  {pdfFile && (
                    <p className="file-info">Fichier sélectionné : {pdfFile.name}</p>
                  )}
                </div>
                <button type="submit" disabled={isLoading || !pdfFile}>
                  {isLoading ? "Traitement en cours..." : "Créer le résumé"}
                </button>
              </form>
            </div>
          )}

          {/* Summarize PDF URL */}
          {activeTab === "pdf-url" && (
            <div className="form-section">
              <h2>Résumer un PDF depuis une URL</h2>
              <form onSubmit={handleSummarizePdfUrl}>
                <div className="form-group">
                  <label>URL du PDF</label>
                  <input
                    type="url"
                    placeholder="https://example.com/document.pdf"
                    value={pdfUrl}
                    onChange={(e) => setPdfUrl(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" disabled={isLoading}>
                  {isLoading ? "Traitement en cours..." : "Créer le résumé"}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;