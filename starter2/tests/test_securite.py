"""Tests de sécurité : authentification (401) et autorisation (403)."""
import pytest

from logiai import config


def test_health_reste_public(client):
    assert client.get("/health").status_code == 200


def test_predict_sans_cle_refuse(client, livraison_valide):
    # Exemple fourni : écrivez les suivants sur ce modèle.
    r = client.post("/v1/predict", json=livraison_valide)
    assert r.status_code == 401


def test_predict_cle_invalide_refuse(client, livraison_valide):
    pytest.fail("À écrire : une mauvaise clé donne 401")


def test_predict_cle_vide_refuse(client, livraison_valide):
    pytest.fail("À écrire : une clé vide donne 401")


def test_predict_cle_utilisateur_accepte(client, headers_user, livraison_valide):
    pytest.fail("À écrire : la clé utilisateur donne 200")


def test_predict_cle_admin_accepte(client, headers_admin, livraison_valide):
    pytest.fail("À écrire : la clé admin donne aussi 200")


def test_model_info_sans_cle_refuse(client):
    pytest.fail("À écrire : /v1/model-info sans clé donne 401")


def test_model_info_cle_utilisateur_interdite(client, headers_user):
    pytest.fail("À écrire : /v1/model-info avec la clé utilisateur donne 403 (et non 401)")


def test_model_info_cle_admin_accepte(client, headers_admin):
    pytest.fail("À écrire : /v1/model-info avec la clé admin donne 200 et contient \"version\"")


def test_la_reponse_401_ne_revele_pas_la_cle(client, livraison_valide):
    pytest.fail("À écrire : le texte de la réponse 401 ne contient aucune des deux vraies clés (config.API_KEY, config.ADMIN_KEY)")


def test_sans_configuration_tout_est_refuse(client, livraison_valide, monkeypatch):
    pytest.fail("À écrire : si config.API_KEY et config.ADMIN_KEY valent None (monkeypatch.setattr), toute clé donne 401")
