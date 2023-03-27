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

def get_mvt_query(table_name: str, z: int, x: int, y: int) -> str:
    """
    Construct the SQL query to fetch the MVT data.
    """
    return f"""
        SELECT ST_AsMVT(q, '{table_name}', 4096, 'geom')
        FROM (
            SELECT osm_id, name, building, ST_AsMVTGeom(
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

@app.get("/api/v1/mvt/{table_name}/{z}/{x}/{y}.mvt", response_class=Response)
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

    query = get_mvt_query(table_name, z, x, y)

    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()[0]
        if result is None:
            response = Response()
        else:
            response = Response(bytes(result), media_type="application/x-protobuf")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
