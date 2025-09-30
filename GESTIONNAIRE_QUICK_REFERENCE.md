# Gestionnaire de Magasin - Carte de Référence Rapide 🟡

## 👤 Rôle : Gestionnaire de Magasin

**Mission principale :** Assurer la gestion globale du magasin et contrôler les mouvements de stock entre l'entrepreneur et le client.

---

## ✅ VOS RESPONSABILITÉS

### 🎯 Gestion Globale du Magasin

#### 1. **Contrôle des Mouvements de Stock**
Vous êtes responsable de la supervision et validation des flux :
- **Entrées** : Réception des pièces de l'entrepreneur/fournisseur
- **Sorties** : Livraison des pièces au client
- **Traçabilité** : Suivi complet de tous les mouvements

#### 2. **Gestion des Références**
- Ajouter de nouvelles références
- Modifier les références existantes
- Supprimer les références obsolètes
- Organiser et optimiser le stock

#### 3. **Supervision des Opérations**
- Surveiller les activités des Consultants (Opérateurs/Caristes)
- Valider les mouvements d'entrées/sorties
- Assurer la conformité des opérations
- Contrôler la qualité des données

#### 4. **Gestion des Zones**
- Créer et organiser les zones de stockage
- Modifier les zones/travées
- Optimiser l'espace de stockage
- Gérer les capacités

---

## 📊 VOS ACCÈS COMPLETS

### ✅ Consultation & Visualisation
- **Dashboard** - Vue complète du stock en temps réel
- **Historique complet** - Tous les mouvements (entrées/sorties)
- **Statistiques** - Analyses et KPIs
- **Recherche avancée** - Filtres par date, référence, fournisseur

### ✅ Opérations de Stock
- **Ajouter référence** - Enregistrer les entrées
- **Saisie sortie** - Enregistrer les sorties
- **Modifier référence** - Corriger les informations
- **Supprimer référence** - Retirer les références obsolètes

### ✅ Gestion & Administration
- **Gestion des références** - CRUD complet
- **Gestion des zones** - Créer, modifier, supprimer les zones
- **Extraction des mouvements** - Générer des rapports personnalisés
- **Export Excel** - Exporter le stock et l'historique
- **Impression** - Imprimer les rapports de stock

### ✅ Fonctionnalités Opérationnelles
- Boot KIT
- Cross DOCK
- Map Débord
- FLC
- Log ext
- How to use it

---

## ❌ RESTRICTIONS

### 🚫 Administration Système
- Créer/modifier/supprimer des utilisateurs
- Accéder à l'interface Django Admin
- Modifier les paramètres système
- → **Réservé aux Administrateurs**

---

## 📱 Votre Interface

### Menu de Navigation Complet
```
┌─────────────────────────────────┐
│ STELLANTIS DIZ                  │
│                                 │
│ 👤 gestionnaire                 │
│ 🟡 Gestionnaire                 │
├─────────────────────────────────┤
│ STOCK & MOUVEMENTS              │
│ 📊 Dashboard                    │
│ ➕ Ajouter Référence (Entrée)   │
│ ➖ Saisie Sortie                │
├─────────────────────────────────┤
│ GESTION & SUPERVISION           │
│ 📦 Gestion Références           │
│ 📜 Historique                   │
│ 📥 Extraction Mouvements        │
│ 🗺️ Gestion Zones                │
├─────────────────────────────────┤
│ FONCTIONNALITÉS                 │
│ 📦 Boot KIT                     │
│ 🔄 Cross DOCK                   │
│ 🗺️ Map Débord                   │
│ 🚚 FLC                          │
│ 📄 Log ext                      │
│ ❓ How to use it                │
├─────────────────────────────────┤
│ PROFIL                          │
│ 👤 Mon Profil                   │
│ 🔑 Mot de passe                 │
│ 🚪 Déconnexion                  │
└─────────────────────────────────┘
```

### Actions Rapides Dashboard
```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│  ➕ Ajouter  │  ➖ Valider  │  📜 Historiq │  📥 Exporter │  🖨️ Imprimer │  ⚙️ Gérer    │
│  Référence   │  Sortie      │  ue          │  Excel       │  Stock       │  Références  │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 🔄 Workflow Type : Contrôle des Mouvements

### Scénario 1 : Réception de Pièces (Entrée)

```
1. Réception physique des pièces de l'entrepreneur/fournisseur
   │
   ▼
2. Connexion au système
   │
   ▼
3. Dashboard → Ajouter Référence
   │
   ▼
4. Saisir les informations :
   - Référence pièce
   - Emplacement SM
   - Nombre de bacs
   - Fournisseur
   - Date d'entrée
   - Travée débord
   │
   ▼
5. Valider l'enregistrement
   │
   ▼
6. Vérifier dans l'Historique
   │
   ▼
7. Confirmation visuelle et système
```

### Scénario 2 : Livraison Client (Sortie)

```
1. Demande de sortie reçue (client)
   │
   ▼
2. Vérifier disponibilité dans le Dashboard
   │
   ▼
3. Saisie Sortie
   │
   ▼
4. Sélectionner la référence
   │
   ▼
5. Indiquer le nombre de bacs à sortir
   │
   ▼
6. Valider la sortie
   │
   ▼
7. Stock automatiquement décrémenté
   │
   ▼
8. Enregistrement dans l'Historique
   │
   ▼
9. Livraison physique au client
```

### Scénario 3 : Supervision Quotidienne

```
1. Connexion matinale
   │
   ▼
2. Consulter Dashboard (KPIs)
   - Total des bacs en stock
   - Nombre de références
   - Alertes stock faible
   │
   ▼
3. Consulter Historique
   - Mouvements de la veille
   - Mouvements du jour
   - Vérifier les anomalies
   │
   ▼
4. Exporter rapport journalier
   - Export Excel de l'historique
   - Filtrer par période
   │
   ▼
5. Vérifier les zones de stockage
   - Gestion Zones
   - Optimisation espace
   │
   ▼
6. Actions correctives si nécessaire
   - Modifier références
   - Réorganiser zones
```

### Scénario 4 : Rapport Mensuel

```
1. Extraction Mouvements
   │
   ▼
2. Définir la période (mois)
   │
   ▼
3. Sélectionner les filtres
   - Type d'action (entrées/sorties)
   - Fournisseurs spécifiques
   │
   ▼
4. Générer l'aperçu
   │
   ▼
5. Exporter en Excel
   │
   ▼
6. Analyser les données
   - Volume entrées vs sorties
   - Principaux fournisseurs
   - Principaux clients
   │
   ▼
7. Rapport de gestion pour direction
```

---

## 📊 Contrôle des Flux Entrepreneur ↔ Client

### Vue d'Ensemble

```
ENTREPRENEUR/FOURNISSEUR
         │
         │ (Entrée)
         ▼
    ┌────────────────┐
    │   VOTRE RÔLE   │
    │   Gestionnaire │ ← Vous contrôlez et validez
    │   de Magasin   │
    └────────────────┘
         │
         │ (Sortie)
         ▼
      CLIENT
```

### Vos Points de Contrôle

1. **À l'Entrée** ✅
   - Vérifier la conformité des pièces reçues
   - Enregistrer les références correctement
   - Affecter les emplacements appropriés
   - Valider les quantités

2. **En Stock** ✅
   - Surveiller les niveaux de stock
   - Identifier les références à risque
   - Optimiser les emplacements
   - Gérer les zones de stockage

3. **À la Sortie** ✅
   - Valider les demandes de sortie
   - Vérifier la disponibilité
   - Enregistrer les mouvements
   - Tracer les livraisons client

4. **Reporting** ✅
   - Historique complet des transactions
   - Exports pour analyses
   - Rapports de performance
   - Statistiques de rotation

---

## 🎯 KPIs à Surveiller

### Indicateurs Quotidiens
- ✅ Nombre d'entrées du jour
- ✅ Nombre de sorties du jour
- ✅ Stock total en bacs
- ✅ Nombre de références actives
- ⚠️ Alertes stock faible

### Indicateurs Hebdomadaires
- 📈 Volume d'entrées vs sorties
- 📊 Taux de rotation des pièces
- 🏢 Principaux fournisseurs
- 👥 Principaux clients
- 📍 Occupation des zones

### Indicateurs Mensuels
- 📑 Rapport complet des mouvements
- 💰 Valeur du stock
- 📦 Références les plus actives
- 🔄 Taux de turnover
- 📉 Références dormantes

---

## 🔐 Responsabilités & Accountability

### Ce dont vous êtes responsable :

✅ **Exactitude des données**
- Toutes les entrées sont correctement enregistrées
- Toutes les sorties sont validées et tracées

✅ **Optimisation du stock**
- Gestion efficace des emplacements
- Rotation optimale des pièces

✅ **Conformité**
- Respect des procédures
- Traçabilité complète

✅ **Supervision**
- Contrôle des opérations des Consultants
- Validation des mouvements

✅ **Reporting**
- Rapports réguliers à la direction
- Analyses de performance

---

## 🆘 Situations d'Exception

### Stock Incohérent
```
1. Consulter Historique
2. Identifier le mouvement problématique
3. Vérifier avec l'Opérateur concerné
4. Corriger via Gestion Références
5. Documenter l'incident
```

### Demande de Sortie > Stock Disponible
```
1. Vérifier stock dans Dashboard
2. Consulter Historique des sorties récentes
3. Contacter le client pour alternatives
4. Coordonner avec fournisseur si nécessaire
5. Mettre à jour les prévisions
```

### Zone de Stockage Pleine
```
1. Gestion Zones → Vérifier capacités
2. Identifier les pièces à rotation lente
3. Réorganiser les emplacements
4. Créer nouvelle zone si nécessaire
5. Mettre à jour la cartographie
```

---

## 📞 Escalation

### Quand contacter l'Administrateur ?
- Besoin de créer un nouveau compte utilisateur
- Problème technique système
- Modification de paramètres globaux
- Accès aux logs système

### Quand impliquer la Direction ?
- Anomalies majeures de stock
- Demandes exceptionnelles client
- Problèmes fournisseurs récurrents
- Décisions stratégiques d'organisation

---

## 🔑 Identifiants de Test

```
Username : gestionnaire
Password : gestionnaire123
Email    : gestionnaire@stellantis.com
Rôle     : Gestionnaire de Magasin
```

---

## 📚 Documentation Complémentaire

- `GUIDE_UTILISATEURS_ROLES.md` - Guide complet des rôles
- `ROLES_HIERARCHY_VISUAL.md` - Hiérarchie visuelle
- `STOCK_DEBORD_README.md` - Documentation technique

---

**Dernière mise à jour :** 29 septembre 2025
**Version :** 1.1

**Vous êtes le pivot central du système de gestion de stock !** 🎯
