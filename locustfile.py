# locustfile.py - Tests de performance selon les specs du projet

from locust import HttpUser, task, between
import random

class GudlftUser(HttpUser):
    """
    Simulateur d'utilisateur pour tester les performances de l'application GUDLFT
    Specs: 6 utilisateurs par défaut, < 5s pour charger compétitions, < 2s pour update points
    """
    
    # Temps d'attente entre les actions (1-3 secondes)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Actions à effectuer au démarrage de chaque utilisateur simulé"""
        # Liste des emails valides pour les tests
        self.valid_emails = [
            "john@simplylift.co",
            "admin@irontemple.com", 
            "kate@shelifts.co.uk"
        ]
        
        # Choisir un email aléatoire pour cet utilisateur
        self.user_email = random.choice(self.valid_emails)
        self.club_name = None
        
    @task(3)  # Poids 3 = plus fréquent
    def load_homepage(self):
        """Test: Chargement de la page d'accueil"""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Homepage returned {response.status_code}")
    
    @task(5)  # Poids 5 = très fréquent
    def load_points_board(self):
        """
        Test CRITIQUE: Chargement du tableau des points (Phase 2)
        SPEC: Doit se charger en moins de 5 secondes
        """
        with self.client.get("/points", catch_response=True) as response:
            # Vérifier le temps de réponse selon les specs
            if response.elapsed.total_seconds() > 5.0:
                response.failure(f"Points board too slow: {response.elapsed.total_seconds():.2f}s (max 5s)")
            elif response.status_code == 200:
                response.success()
            else:
                response.failure(f"Points board returned {response.status_code}")
    
    @task(4)  # Poids 4 = fréquent
    def user_login_flow(self):
        """Test: Workflow complet de connexion utilisateur"""
        # 1. Connexion avec email valide
        login_response = self.client.post("/showSummary", data={
            "email": self.user_email
        }, catch_response=True)
        
        if login_response.status_code == 200:
            login_response.success()
            # Extraire le nom du club pour les tests suivants
            if b"Simply Lift" in login_response.content:
                self.club_name = "Simply Lift"
            elif b"Iron Temple" in login_response.content:
                self.club_name = "Iron Temple"
            elif b"She Lifts" in login_response.content:
                self.club_name = "She Lifts"
        else:
            login_response.failure(f"Login failed with {login_response.status_code}")
    
    @task(2)  # Poids 2 = moins fréquent
    def booking_flow(self):
        """
        Test CRITIQUE: Processus de réservation complet
        SPEC: Update des points doit prendre moins de 2 secondes
        """
        if not self.club_name:
            return  # Skip si pas connecté
            
        # 1. Aller sur page de réservation
        book_page = self.client.get(f"/book?competition=Spring Festival&club={self.club_name}")
        
        if book_page.status_code != 200:
            return
            
        # 2. Faire une réservation (test de mise à jour des points)
        booking_data = {
            "club": self.club_name,
            "competition": "Spring Festival",
            "places": "1"  # Petite réservation pour ne pas épuiser les points
        }
        
        with self.client.post("/purchasePlaces", data=booking_data, catch_response=True) as response:
            # Vérifier le temps de réponse selon les specs  
            if response.elapsed.total_seconds() > 2.0:
                response.failure(f"Points update too slow: {response.elapsed.total_seconds():.2f}s (max 2s)")
            elif response.status_code in [200, 302]:  # 302 = redirection OK
                response.success()
            else:
                response.failure(f"Booking failed with {response.status_code}")
    
    @task(1)  # Poids 1 = rare
    def test_error_cases(self):
        """Test des cas d'erreur pour vérifier la robustesse"""
        # Test email invalide (ne doit pas crasher)
        error_response = self.client.post("/showSummary", data={
            "email": "nonexistent@test.com"
        }, catch_response=True)
        
        # Doit gérer l'erreur gracieusement (pas de 500)
        if error_response.status_code == 500:
            error_response.failure("App crashed on invalid email (Issue 1 not fixed)")
        else:
            error_response.success()
    
    @task(1)
    def logout_flow(self):
        """Test: Déconnexion utilisateur"""
        logout_response = self.client.get("/logout")
        # La déconnexion doit rediriger vers l'accueil
        if logout_response.status_code in [200, 302]:
            pass  # OK

# === CONFIGURATION POUR LES SPECS DU PROJET ===
# Par défaut, Locust utilisera:
# - 6 utilisateurs simultanés (selon les specs)
# - Montée en charge progressive
# - Tests des temps de réponse critiques (5s et 2s)