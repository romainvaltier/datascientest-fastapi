# datascientest-fastapi

## Besoins

1. L'application ou le navigateur Web, l'utilisateur doit pouvoir choisir un type de test (use) ainsi qu'une ou plusieurs catégories (subject).
1. L'application peut produire des QCMs de 5, 10 ou 20 questions. L'API doit donc être en mesure de retourner ce nombre de questions.
1. Comme l'application doit pouvoir générer de nombreux QCMs, les questions doivent être retournées dans un ordre aléatoire: ainsi, une requête avec les mêmes paramètres pourra retourner des questions différentes.
1. Les utilisateurs devant avoir créé un compte, il faut que nous soyons en mesure de vérifier leurs identifiants.
1. Pour l'instant l'API utilise une authentification basique, à base de nom d'utilisateur et de mot de passe: la chaîne de caractères contenant **Basic username:password** devra être passée dans l'en-tête **Authorization** (en théorie, cette chaîne de caractère devrait être encodée mais pour simplifier l'exercice, on peut choisir de ne pas l'encoder)
1. Pour les identifiants, on pourra utiliser le dictionnaire suivant:

    ```python
    {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
    }
    ```

1. L'API devra aussi implémenter un point de terminaison pour vérifier que l'API est bien fonctionnelle.
1. Permettre à un utilisateur **admin** dont le mot de passe est **4dm1N** de créer une nouvelle question.
