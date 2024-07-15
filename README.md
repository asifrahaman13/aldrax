## Contribution guidelines  👨🏻‍🚀

![Screenshot from 2024-07-15 20-56-59](https://github.com/user-attachments/assets/f7ac3f35-9be1-4c69-90ef-2fe3d9026faa)
![Screenshot from 2024-07-15 20-56-22](https://github.com/user-attachments/assets/b8908893-2150-4dff-814e-934e65809054)
![Screenshot from 2024-07-15 20-58-27](https://github.com/user-attachments/assets/eddbaf9f-7ec7-47a0-bf15-c362f25e7227)


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
