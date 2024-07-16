## About the application 👨🏻‍🚀

Full stack application to io interact with sample sqlite database.

![Screenshot from 2024-07-16 23-02-06](https://github.com/user-attachments/assets/73b40d29-56db-4e78-b8ee-a591cc709b3f)

![Screenshot from 2024-07-16 23-14-50](https://github.com/user-attachments/assets/e74fcef3-0c26-48cb-8997-b9eb8206f76a)

![Screenshot from 2024-07-16 22-53-11](https://github.com/user-attachments/assets/c1b850be-3112-4bcb-91ff-a91c342100f3)

![Screenshot from 2024-07-16 22-57-03](https://github.com/user-attachments/assets/b81f25b0-ea4f-466a-9bf5-9a4aa16a15ec)



- First, pull the repository. `git clone https://github.com/asifrahaman13/aldrax.git`

- Go to the root directory. `cd aldrax`

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
