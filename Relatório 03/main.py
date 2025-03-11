from database import Database
from writeAJson import writeAJson

db = Database(database="pokedex", collection="pokemons")
db.resetDatabase()