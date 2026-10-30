from fastapi import FastAPI

app = FastAPI(title="Prévision de trafic télécom")


@app.get("/health")
def health():
    return {"status": "ok"}

# TODO: /forecast une fois le meilleur modèle choisi et sauvegardé dans models/
