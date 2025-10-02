import { useState } from "react";
import { useNavigate } from "react-router-dom";
import './login.css';

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);
      
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessage("Connexion réussie ! Redirection...");
        setMessageType("success");
        
        // Stocker le token
        localStorage.setItem("token", data.access_token);
        
        // Redirection immédiate vers le dashboard
        setTimeout(() => {
          navigate("/dashboard");
        }, 500);
      } else {
        const error = await response.json();
        setMessage("Erreur : " + error.detail);
        setMessageType("error");
      }
    } catch {
      setMessage("Impossible de joindre le serveur");
      setMessageType("error");
    }
  };

  return (
    <div>
      <header>
        <h1>Bienvenue sur LexiTrack</h1>
      </header>
      <form onSubmit={handleLogin}>
        <h2>Connexion</h2>
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
        <button type="submit">Se connecter</button>
        {message && <p className={messageType}>{message}</p>}
        <div className="register-link">
          <p>Pas encore de compte ? <a href="/register">S'inscrire</a></p>
        </div>
      </form>
    </div>
  );
}

export default Login;