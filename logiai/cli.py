"""Interface en ligne de commande pour prédire le retard d'une livraison."""

import argparse
import json
import sys
from pathlib import Path

from logiai.config import ALERT_THRESHOLD
from logiai.predict import Predictor


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="logiai-predict")
    parser.add_argument("fichier", help="fichier JSON d'une livraison")
    args = parser.parse_args(argv)
    chemin = Path(args.fichier)
    if not chemin.exists():
        print(f"Fichier introuvable : {chemin}", file=sys.stderr)
        return 1
    livraison = json.loads(chemin.read_text(encoding="utf-8"))
    resultat = Predictor().predict(livraison)
    proba = resultat["probabilite_retard"]
    statut = "ALERTE" if proba >= ALERT_THRESHOLD else "OK"
    print(f"Probabilité de retard : {round(proba * 100)} % ({statut})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

