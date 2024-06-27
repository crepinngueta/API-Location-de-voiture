## Application de location de voiture sans chauffeur

Ce projet est une API d'authentification construite avec Django Rest Framework et Simple JWT. Elle comprend des fonctionnalités telles que l'inscription d'utilisateurs, la connexion avec un modèle utilisateur personnalisé, le changement de mot de passe et la réinitialisation du mot de passe par e-mail. L'API utilise Simple JWT pour l'authentification par token.

## Fonctionnalités

- Inscription d'utilisateur avec modèle utilisateur personnalisé
- Connexion d'utilisateur avec modèle utilisateur personnalisé
- Changement de mot de passe pour les utilisateurs authentifiés
- Réinitialisation du mot de passe par e-mail
- Authentification par token Simple JWT

## Référence de l'API

| URL                                      | Méthode | Description                                |
| ---------------------------------------- | ------- | ------------------------------------------ |
| `api/user/register/`                     | `POST`  | **Enregistrer un nouvel utilisateur**      |
| `api/user/login/`                        | `POST`  | **Connexion de l'utilisateur avec des identifiants valides et un jeton d'authentification** |
| `api/user/profile/`                      | `GET`   | **Affiche la page de profil de l'utilisateur** |
| `api/user/changepassword/`               | `POST`  | **Changer le mot de passe de l'utilisateur** |
| `api/user/send-reset-password-email/`    | `POST`  | **Envoyer l'e-mail de réinitialisation du mot de passe** |
| `api/user/reset-password/<uidb64>/<token>/` | `POST` | **URL pour le changement de mot de passe** |

## Autres fonctionnalités à implémenter

- Ajout de véhicule à la location
- Modification d'un véhicule
- Suppression d'un véhicule
- Affichage de tous les véhicules (peu importe le propriétaire, mais l'utilisateur doit être connecté)
- Affichage des détails d'un véhicule
- Gestion des réservations de véhicules
- Gestion des paiements pour les réservations