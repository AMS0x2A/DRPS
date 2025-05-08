debug:
	@python3 -m src.main -d -p 14642 

drps:
	@gunicorn -w 4 -b localhost 'src.app:create_app()'

docker:
	@docker build --tag drps-app .;
	@docker run --name drps-app --rm -d -p 14642:14642 drps-app;