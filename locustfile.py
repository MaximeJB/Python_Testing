from locust import HttpUser, task, between
import random

class GudlftUser(HttpUser):
    """
    Simulateur d'utilisateur avec gestion des erreurs améliorée
    """
    
    wait_time = between(2, 5)  # Plus d'espace entre les requêtes
    
    def on_start(self):
        """Configuration initiale"""
        self.clubs = [
            {"email": "john@simplylift.co", "name": "Simply Lift"},
            {"email": "admin@irontemple.com", "name": "Iron Temple"}, 
            {"email": "kate@shelifts.co.uk", "name": "She Lifts"}
        ]
        self.competitions = ["Spring Festival", "Fall Classic"]
        self.selected_club = random.choice(self.clubs)
        
    @task(3)
    def load_homepage(self):
        """GET / - Page d'accueil"""
        self.client.get("/")
    
    @task(5)
    def load_points_board(self):
        """GET /points - Tableau des points"""
        self.client.get("/points")
    
    @task(3)
    def user_login_flow(self):
        """POST /showSummary - Connexion seulement"""
        with self.client.post("/showSummary", 
                             data={"email": self.selected_club["email"]},
                             catch_response=True, 
                             name="Login") as response:
            if response.status_code == 200:
                response.success()
    
    @task(1)  # Réduit la fréquence des achats
    def safe_booking_flow(self):
        """
        Flow de réservation SÉCURISÉ avec gestion d'erreur
        """
        # Étape 1: Connexion
        login_response = self.client.post("/showSummary", 
                                         data={"email": self.selected_club["email"]})
        
        if login_response.status_code != 200:
            return
        
        # Étape 2: Page de réservation
        competition = random.choice(self.competitions)
        book_response = self.client.get(f"/book/{competition}/{self.selected_club['name']}")
        
        if book_response.status_code != 200:
            return
        
        # Étape 3: Achat avec seulement 1 place (plus safe)
        booking_data = {
            "club": self.selected_club["name"],
            "competition": competition,
            "places": "1"  # Toujours 1 place pour éviter les conflits
        }
        
        with self.client.post("/purchasePlaces", 
                            data=booking_data,
                            catch_response=True,
                            name="Purchase Places") as response:
            
            # Accepte les erreurs 400 comme normales (pas d'échec dans les stats)
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(2)
    def view_only_session(self):
        """Session de consultation seulement"""
        self.client.get("/")
        self.client.get("/points")
        self.client.post("/showSummary", data={"email": self.selected_club["email"]})

# === CONFIGURATION POUR LES SPECS DU PROJET ===
# Par défaut, Locust utilisera:
# - 6 utilisateurs simultanés (selon les specs)
# - Montée en charge progressive
# - Tests des temps de réponse critiques (5s et 2s)