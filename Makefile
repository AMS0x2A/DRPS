debug:
	@python3 -m src.main -d -p 14642 

drps:
	@gunicorn -w 4 -b 0.0.0.0:14642 'src.app:create_app()'

docker:
	@docker build --tag drps .;
	@docker run --name drps --rm -d -p 14642:14642 drps;