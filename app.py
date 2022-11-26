# use FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from pdf import process
from io import BytesIO


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./static/html/index.html") as f:
        data = f.read()
    return HTMLResponse(content=data)


@app.get("/api")
def generate_pdf(characters: str = ""):
    if characters == "":
        return

    characters = characters[:100]

    try:
      pdf = process(characters)
      if (pdf is None):
          return

      pdf_io = BytesIO(pdf.encode('latin-1'))
      pdf_io.seek(0)

      res =  StreamingResponse(pdf_io, media_type="application/pdf")
      res.headers["Content-Disposition"] = f"attachment; filename={characters}.pdf"

      return res
    except Exception as e:
        print(e)
        return


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
