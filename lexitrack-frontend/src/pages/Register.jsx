import { useState } from "react";
import { useNavigate } from "react-router-dom";
import './Register.css';

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    
    // Validation des mots de passe
    if (password !== confirmPassword) {
      setMessage("Erreur : Les mots de passe ne correspondent pas");
      setMessageType("error");
      return;
    }

    if (password.length < 6) {
      setMessage("Erreur : Le mot de passe doit contenir au moins 6 caractères");
      setMessageType("error");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/users/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("Inscription réussie ! Redirection vers la connexion...");
        setMessageType("success");
        
        // Réinitialiser le formulaire
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        
        // Redirection vers la page de connexion après 1.5 secondes
        setTimeout(() => {
          navigate("/login");
        }, 1500);
      } else {
        const error = await response.json();
        if (error.detail === "This user already exist") {
          setMessage("Erreur : Cet utilisateur existe déjà");
        } else {
          setMessage("Erreur : " + error.detail);
        }
        setMessageType("error");
      }
    } catch {
      setMessage("Erreur : Impossible de joindre le serveur");
      setMessageType("error");
    }
  };

  return (
    <div>
      <header>
        <h1>Bienvenue sur LexiTrack</h1>
      </header>
      <form onSubmit={handleRegister}>
        <h2>Créer un compte</h2>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Confirmer le mot de passe"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">S'inscrire</button>
        {message && <p className={messageType}>{message}</p>}
        <div className="login-link">
          <p>Déjà un compte ? <a href="/login">Se connecter</a></p>
        </div>
      </form>
    </div>
  );
}

export default Register;