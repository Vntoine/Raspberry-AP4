<h1 align="center">📋 Raspberry AP4 📋</h1>
<p>Application Python utilisant une raspberry, un lecteur RFID et une caméra</p>
<p>Interface de connexion en trois grandes étapes :</p>
<ul>
    <li>Authentification login/password à l'aide d'une API REST</li>
    <li>Passage de la carte d'accès associée au couple précédent sur le lecteur RFID, vérification avec un second appel API REST </li>
    <li>Reconnaissance faciale</li>
</ul>
<p>Un afficheur LED (microbit) permet à l'utilisateur de visualiser la validation d'une étape d'authentification ✔️❌</p>
<p>Enregistrements (logs) tout au long de l'authentification dans une base de données SQLite3 🗃</p>
