"""Tester pour casser : valeurs limites et entrées malformées.

Le projet contient 2 bugs volontaires dans les bornes. Vos tests doivent les trouver.
"""
import pytest

# (champ, valeur envoyée, code attendu) : on teste les DEUX côtés de chaque borne
CAS_LIMITES = [
    ("distance_km", 1, 200), ("distance_km", 0.9, 422),
    ("distance_km", 1000, 200), ("distance_km", 1001, 422),
    # À VOUS : ajoutez les deux côtés de chaque borne pour les 6 autres champs.
    # Pensez aussi aux entiers : 11.5 est-il une heure valide ?
]


@pytest.mark.parametrize("champ, valeur, attendu", CAS_LIMITES)
def test_valeurs_limites(client, headers_user, livraison_valide, champ, valeur, attendu):
    livraison_valide[champ] = valeur
    r = client.post("/v1/predict", json=livraison_valide, headers=headers_user)
    assert r.status_code == attendu, f"{champ}={valeur} : attendu {attendu}, obtenu {r.status_code}"
