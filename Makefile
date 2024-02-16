install:
	apt update
	apt install python3
	apt install pipx
	pipx ensurepath
	pipx install poetry
	poetry install

start:
	poetry run start