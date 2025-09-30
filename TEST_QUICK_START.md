# 🚀 TEST RAPIDE - Système d'Utilisateurs et Rôles

## ⚡ Démarrage en 3 étapes

### Étape 1: Vérifier que le serveur est lancé
```bash
# Si pas déjà lancé:
py manage.py runserver
```

### Étape 2: Accéder à l'application
```
http://localhost:8000/auth/login/
```

### Étape 3: Tester les 3 comptes

## 🧪 Tests à Effectuer

### TEST 1: Connexion en tant qu'ADMIN

1. **Se connecter:**
   - Username: `admin`
   - Password: `admin123`

2. **Vérifier dans la sidebar:**
   - ✅ Badge "Administrateur" (rouge) sous votre nom
   - ✅ Lien "Gestion Utilisateurs" visible
   - ✅ Lien "Admin Django" visible
   - ✅ Lien "Mon Profil" visible
   - ✅ Lien "Déconnexion" visible

3. **Tester Gestion Utilisateurs:**
   - Cliquer sur "Gestion Utilisateurs"
   - ✅ Voir la liste des 3 utilisateurs (admin, gestionnaire, consultant)
   - Cliquer sur "Nouvel Utilisateur"
   - ✅ Formulaire de création s'affiche
   - Essayer de créer un utilisateur test
   - ✅ Utilisateur créé avec succès

4. **Tester Mon Profil:**
   - Cliquer sur "Mon Profil"
   - ✅ Voir vos informations
   - ✅ Voir la liste des permissions Admin

---

### TEST 2: Connexion en tant que GESTIONNAIRE

1. **Se déconnecter puis se connecter:**
   - Username: `gestionnaire`
   - Password: `gestionnaire123`

2. **Vérifier dans la sidebar:**
   - ✅ Badge "Gestionnaire de magasin" (jaune) sous votre nom
   - ❌ Lien "Gestion Utilisateurs" PAS visible
   - ❌ Lien "Admin Django" PAS visible
   - ✅ Lien "Mon Profil" visible
   - ✅ Lien "Déconnexion" visible

3. **Tester l'accès refusé:**
   - Essayer d'accéder manuellement: `http://localhost:8000/auth/users/`
   - ✅ Message: "Vous n'avez pas les permissions nécessaires"
   - ✅ Redirection vers le dashboard

4. **Tester Mon Profil:**
   - Cliquer sur "Mon Profil"
   - ✅ Voir les permissions Gestionnaire

---

### TEST 3: Connexion en tant que CONSULTANT

1. **Se déconnecter puis se connecter:**
   - Username: `consultant`
   - Password: `consultant123`

2. **Vérifier dans la sidebar:**
   - ✅ Badge "Consultant (Opérateur/Cariste)" (bleu) sous votre nom
   - ❌ Lien "Gestion Utilisateurs" PAS visible
   - ❌ Lien "Admin Django" PAS visible
   - ✅ Lien "Mon Profil" visible
   - ✅ Lien "Déconnexion" visible

3. **Tester l'accès refusé:**
   - Essayer d'accéder manuellement: `http://localhost:8000/auth/users/`
   - ✅ Message d'erreur et redirection

4. **Tester Mon Profil:**
   - Cliquer sur "Mon Profil"
   - ✅ Voir les permissions Consultant (plus limitées)

---

## ✅ Checklist de Validation

### Interface
- [ ] Badge de rôle visible avec la bonne couleur
- [ ] Nom d'utilisateur affiché correctement
- [ ] Menu "Gestion Utilisateurs" visible pour Admin uniquement
- [ ] Menu "Admin Django" visible pour Admin uniquement
- [ ] Menus "Mon Profil" et "Déconnexion" pour tous

### Fonctionnalités Admin
- [ ] Créer un utilisateur fonctionne
- [ ] Modifier un utilisateur fonctionne
- [ ] Supprimer un utilisateur fonctionne
- [ ] Liste des utilisateurs s'affiche correctement
- [ ] Filtres et recherche fonctionnent

### Sécurité
- [ ] Gestionnaire ne peut pas accéder à /auth/users/
- [ ] Consultant ne peut pas accéder à /auth/users/
- [ ] Admin ne peut pas supprimer son propre compte
- [ ] Messages d'erreur appropriés affichés

### Profil Utilisateur
- [ ] Profil s'affiche avec les bonnes informations
- [ ] Changement de mot de passe fonctionne
- [ ] Permissions listées correspondent au rôle

---

## 🎯 Scénario Complet

### Créer un Nouvel Utilisateur (En tant qu'Admin)

1. Connexion: `admin` / `admin123`
2. Sidebar → "Gestion Utilisateurs"
3. Bouton "Nouvel Utilisateur"
4. Remplir:
   ```
   Username: test_user
   Email: test@stellantis.com
   Rôle: Consultant
   Password: Test123!
   Password (confirmation): Test123!
   ```
5. Cliquer "Créer l'utilisateur"
6. ✅ Message de succès
7. ✅ Retour à la liste avec le nouvel utilisateur

### Tester le Nouveau Compte

1. Se déconnecter
2. Se connecter avec: `test_user` / `Test123!`
3. ✅ Connexion réussie
4. ✅ Badge "Consultant" visible
5. ✅ Accès limité (pas de gestion utilisateurs)

### Modifier un Utilisateur (En tant qu'Admin)

1. Connexion: `admin` / `admin123`
2. Gestion Utilisateurs
3. Cliquer sur ✏️ à côté de "test_user"
4. Changer le rôle: Consultant → Gestionnaire
5. Sauvegarder
6. ✅ Modification enregistrée

### Vérifier le Changement

1. Se déconnecter
2. Se reconnecter: `test_user` / `Test123!`
3. ✅ Badge maintenant "Gestionnaire" (jaune)

---

## 🔍 Résolution de Problèmes

### "Je ne vois pas le lien Gestion Utilisateurs"
**Solution:**
1. Vérifiez que vous êtes connecté avec `admin`
2. Regardez le badge: doit afficher "Administrateur"
3. Rafraîchissez la page (F5)
4. Videz le cache du navigateur (Ctrl+Shift+R)

### "Le badge ne s'affiche pas"
**Solution:**
1. Assurez-vous que Font Awesome est chargé
2. Vérifiez la console du navigateur (F12)
3. Rafraîchissez la page

### "Erreur 404 sur /auth/users/"
**Solution:**
1. Vérifiez que le serveur est lancé
2. Vérifiez que vous êtes authentifié
3. Vérifiez les URLs dans `apps/authentication/urls.py`

### "Permission refusée alors que je suis Admin"
**Solution:**
```bash
# Vérifier le rôle dans Django shell
py manage.py shell
>>> from apps.authentication.models import CustomUser
>>> user = CustomUser.objects.get(username='admin')
>>> print(f"Role: {user.role}")
>>> print(f"Is admin: {user.is_admin()}")

# Si le rôle n'est pas 'admin', le corriger:
>>> user.role = 'admin'
>>> user.save()
```

---

## 📸 À Quoi Ça Doit Ressembler

### Sidebar Admin
```
╔══════════════════╗
║ STELLANTIS DIZ   ║
║                  ║
║    👤            ║
║    admin         ║
║ [Administrateur] ║ ← Badge rouge
║                  ║
║ ──────────────── ║
║ Dashboard        ║
║ ...              ║
║ How to use it    ║
║ ──────────────── ║
║ 👥 Gestion       ║ ← Visible
║    Utilisateurs  ║
║ 🛠️ Admin Django  ║ ← Visible
║ ──────────────── ║
║ 👤 Mon Profil    ║
║ 🔑 Mot de passe  ║
║ 🚪 Déconnexion   ║
╚══════════════════╝
```

### Sidebar Gestionnaire
```
╔══════════════════╗
║ STELLANTIS DIZ   ║
║                  ║
║    👤            ║
║  gestionnaire    ║
║ [Gestionnaire    ║ ← Badge jaune
║  de magasin]     ║
║                  ║
║ ──────────────── ║
║ Dashboard        ║
║ ...              ║
║ How to use it    ║
║ ──────────────── ║
║ 👤 Mon Profil    ║ ← Pas de section Admin
║ 🔑 Mot de passe  ║
║ 🚪 Déconnexion   ║
╚══════════════════╝
```

---

## 🎉 Succès!

Si tous les tests passent, votre système d'utilisateurs et de rôles est **100% fonctionnel**!

Prochaines étapes:
1. ✅ Créer vos utilisateurs réels
2. ✅ Supprimer les comptes de test (en production)
3. ✅ Personnaliser les permissions selon vos besoins
4. ✅ Ajouter plus de fonctionnalités spécifiques aux rôles

---

**Bon test! 🚀**
