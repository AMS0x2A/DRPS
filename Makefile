debug:
	@python3 -m src.main -d -p 8080 

drps:
	@gunicorn -w 4 -b 0.0.0.0 'src.app:create_app()'

docker:
	@docker build --tag drps-app .;
	@docker run --name drps-app --rm -d -p 8000:5000 drps-app;