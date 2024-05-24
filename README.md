# WLapi

`connection-string` in `.env` you should write `connection_string = "postgresql+psycopg2://docker:docker@localhost:5432/wldatabase"`

to run docker run this command `docker-compose -f .\docker-compose.yaml up`


to run the app run this command `uvicorn src.app.main:app --reload`
