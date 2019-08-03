from app import app
from dotenv import load_dotenv

load_dotenv()
app.run(host="localhost", port=1337, debug=True)
