## About the application 👨🏻‍🚀

![Screenshot from 2024-07-15 23-06-05](https://github.com/user-attachments/assets/3fba2072-8970-4ebe-b843-78b71d38f3c1)

![Screenshot from 2024-07-15 23-08-21](https://github.com/user-attachments/assets/730e8195-960c-4189-aa4f-0fab064d02ff)

![Screenshot from 2024-07-15 23-10-16](https://github.com/user-attachments/assets/94cbcdf2-3e66-4306-85b1-b4fd5b1778b2)

![Screenshot from 2024-07-15 23-13-38](https://github.com/user-attachments/assets/7b014cab-75bb-4e6b-b596-acac5b18a2db)


- First, pull the repository. `git clone https://github.com/asifrahaman13/aldrax.git`

- Go to the root directory. `cd superquery`

- Enable virtual environment for the poetry. `poetry config virtualenvs.in-project true`

- Now install the dependencies. `poetry install`

- Now rename the .env.example. `mv .env.example .env`.  Give the proper configuration by giving the API keys. For example set the open ai key etc. Also set the configuration data in the config.yaml file.

## Install precommit hooks.

You need to install the pre-commit hooks to ensure that your code follows the proper guidelines and linting.

 `poetry run pre-commit install`

# Run the server 🚀
You need to run the application using the following script: `poetry run uvicorn src.main:app --reload`

## Frontend

Next go to the front end folder 

`cd frontend/`

Now, install the dependencies.

`bun install`

Next, you can run the code.

`bun run dev`

Now rename .env.example to .env file.

`mv .env.example .env`


## Run with docker

The best way of utilizing the docker is through the docker-compose file.

`docker compose up -d`


## PORT 👨🏻‍🚀

- Backend: 8000
- Frontend: 3000
