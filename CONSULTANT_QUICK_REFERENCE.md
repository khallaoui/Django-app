# Consultant - Carte de Référence Rapide 🔵

## 👤 Rôle : Consultant (Opérateur / Cariste)

---

## ✅ VOUS POUVEZ

### 📊 Consulter
- **Dashboard** - Voir tout le stock en temps réel
- **Stock** - Rechercher et filtrer les références

### ➕ Ajouter (Entrées)
- **Ajouter Référence** - Enregistrer de nouvelles entrées de pièces
- **Remplir les informations** :
  - Référence
  - Emplacement SM
  - Nombre de bacs
  - Fournisseur
  - Etc.

### ➖ Sorties
- **Saisie Sortie** - Enregistrer les sorties de pièces
- **Valider les sorties** - Décrémenter le stock

### 🔧 Fonctionnalités Opérationnelles
- Boot KIT
- Cross DOCK
- Map Débord
- FLC
- Log ext
- How to use it

### 👤 Profil
- Consulter votre profil
- Changer votre mot de passe

---

## ❌ VOUS NE POUVEZ PAS

### 🚫 Historique
- Consulter l'historique complet des mouvements
- → **Réservé aux Gestionnaires et Admins**

### 🚫 Exports
- Exporter le stock en Excel
- Exporter l'historique
- Extraire les mouvements
- Imprimer le stock
- → **Réservé aux Gestionnaires et Admins**

### 🚫 Gestion
- Gérer les références (modifier/supprimer)
- Gérer les zones/travées
- → **Réservé aux Gestionnaires et Admins**

### 🚫 Administration
- Créer/modifier/supprimer des utilisateurs
- Accéder à l'interface Django Admin
- → **Réservé aux Administrateurs**

---

## 📱 Navigation

### Menu Latéral (Ce que vous voyez)
```
┌─────────────────────────────────┐
│ STELLANTIS DIZ                  │
│                                 │
│ 👤 consultant                   │
│ 🔵 Consultant                   │
├─────────────────────────────────┤
│ 📊 Dashboard                    │
│ ➕ Ajouter Référence (Entrée)   │
│ ➖ Saisie Sortie                │
├─────────────────────────────────┤
│ 📦 Boot KIT                     │
│ 🔄 Cross DOCK                   │
│ 🗺️ Map Débord                   │
│ 🚚 FLC                          │
│ 📄 Log ext                      │
│ ❓ How to use it                │
├─────────────────────────────────┤
│ 👤 Mon Profil                   │
│ 🔑 Mot de passe                 │
│ 🚪 Déconnexion                  │
└─────────────────────────────────┘
```

### Actions Rapides Dashboard
```
┌──────────────────┬──────────────────┐
│   ➕ Ajouter     │   ➖ Valider     │
│   Référence      │   Sortie         │
└──────────────────┴──────────────────┘
```

---

## 🔐 Sécurité

Si vous essayez d'accéder à une page non autorisée :
1. ⚠️ Vous serez redirigé vers le Dashboard
2. 📢 Un message d'erreur s'affichera :
   > "Vous n'avez pas les permissions nécessaires pour accéder à cette page."

---

## 📝 Workflow Typique

### 1️⃣ Connexion
```
1. Aller sur /auth/login/
2. Entrer username : consultant
3. Entrer password : consultant123
4. Cliquer sur "Se connecter"
```

### 2️⃣ Consulter le Stock
```
1. Vous êtes sur le Dashboard
2. Voir les KPIs (Total bacs, Total références)
3. Utiliser la recherche et les filtres
4. Parcourir les pages avec la pagination
```

### 3️⃣ Ajouter une Entrée
```
1. Cliquer sur "Ajouter Référence"
2. Remplir le formulaire :
   - Emplacement SM
   - Référence
   - Nombre de bacs
   - Date d'entrée
   - Travée débord
   - Fournisseur
   - Code condi
   - Qt pièce/UC
   - Appro
   - CMJ
   - F
3. Cliquer sur "Enregistrer"
4. Confirmation : "Référence ajoutée avec succès!"
```

### 4️⃣ Enregistrer une Sortie
```
1. Cliquer sur "Saisie Sortie"
2. Sélectionner la référence
3. Entrer le nombre de bacs
4. Cliquer sur "Valider la sortie"
5. Confirmation : "Sortie de X bacs enregistrée!"
```

### 5️⃣ Déconnexion
```
1. Cliquer sur "Déconnexion" en bas du menu
2. Vous êtes redirigé vers la page de connexion
```

---

## 🆘 Besoin d'Aide ?

### Questions Fréquentes

**Q: Pourquoi je ne vois pas l'historique ?**
> A: L'historique complet est réservé aux Gestionnaires et Admins. Vous pouvez consulter le stock actuel sur le Dashboard.

**Q: Comment puis-je exporter les données ?**
> A: Les exports sont réservés aux Gestionnaires et Admins. Contactez votre responsable si vous avez besoin d'un export.

**Q: Je ne peux pas modifier une référence ?**
> A: La gestion des références est réservée aux Gestionnaires et Admins. Pour modifier une référence, contactez votre responsable.

**Q: J'ai oublié mon mot de passe ?**
> A: Contactez votre administrateur pour réinitialiser votre mot de passe.

---

## 📞 Contacts

- **Gestionnaire de Magasin** - Pour les demandes de modifications, exports, etc.
- **Administrateur** - Pour les problèmes de compte, réinitialisation de mot de passe

---

## 🔑 Identifiants de Test

```
Username : consultant
Password : consultant123
Email    : consultant@stellantis.com
Rôle     : Consultant (Opérateur / Cariste)
```

---

**Dernière mise à jour :** 29 septembre 2025
**Version :** 1.1
