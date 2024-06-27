from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User  # Importation du modèle d'utilisateur personnalisé

class UserModelAdmin(BaseUserAdmin):
    
    # Les champs à afficher dans l'administration pour le modèle User.
    # Ils remplacent les définitions de base de UserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ["id", "email", "name", "tc", "is_admin"]  # Champs affichés dans la liste des utilisateurs
    list_filter = ["is_admin"]  # Filtre pour les utilisateurs administrateurs
    fieldsets = [
        ("Informations de connexion", {"fields": ["email", "password"]}),  # Section pour les informations de connexion
        ("Informations personnelles", {"fields": ["name", "tc"]}),  # Section pour les informations personnelles
        ("Permissions", {"fields": ["is_admin"]}),  # Section pour les permissions
    ]
    # add_fieldsets n'est pas un attribut standard de ModelAdmin. UserAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],  # Champs à afficher lors de l'ajout d'un utilisateur
            },
        ),
    ]
    search_fields = ["email"]  # Champ utilisé pour la recherche d'utilisateurs par email
    ordering = ["email", "id"]  # Ordre de tri des utilisateurs dans l'administration
    filter_horizontal = []  # Utilisé pour des champs de type ManyToMany

# Enregistrer le nouveau UserAdmin...
admin.site.register(User, UserModelAdmin)  # Enregistrement du modèle d'utilisateur personnalisé dans l'administration Django
