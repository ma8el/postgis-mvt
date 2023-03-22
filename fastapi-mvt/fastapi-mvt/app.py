import io

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import psycopg2
import psycopg2.extras

app = FastAPI()

db_host = "localhost"
db_port = 5432
db_name = "mydb"
db_user = "markuskurbel"
db_password = ""

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mvt/{table_name}/{z}/{x}/{y}.mvt", response_class=Response)
async def get_mvt(table_name: str, z: int, x: int, y: int) -> Response:
    """
    Get MVT data for a specific table and tile coordinates.
    """
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    # Construct the SQL query to fetch the MVT data
    query = f"""
        SELECT ST_AsMVT(q, '{table_name}', 4096, 'geom')
        FROM (
            SELECT id, ST_AsMVTGeom(
                geom,
                ST_TileEnvelope({z}, {x}, {y}),
                4096,
                256,
                true
            ) AS geom
            FROM {table_name}
            WHERE ST_Intersects(
                geom,
                ST_TileEnvelope({z}, {x}, {y})
            )
        ) AS q
    """

    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()[0]
        if result is None:
            response = Response()
        else:
            response = Response(bytes(result), media_type="application/x-protobuf")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
