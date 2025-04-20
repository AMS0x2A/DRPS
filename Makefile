debug:
	@source venv/bin/activate;
	@python3 src/main.py -d -p 8080 

drps:
	@source venv/bin/activate;
	@gunicorn -w 4 -b 0.0.0.0 'src.app:create_app()'

docker:
	@docker build --tag drps-app .;
	@docker run --name drps-app --rm -d -p 8000:5000 drps-app;