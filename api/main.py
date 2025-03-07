from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "eita porra dum caralho agora fudeu de vez"}
