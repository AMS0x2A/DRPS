debug:
	@echo "This doesn't work unless internal imports are relative"
	@python3 src/main.py -d -p 8080 

drps:
	@gunicorn -w 4 -b 0.0.0.0 'src.app:create_app()'

docker:
	@docker build --tag drps-app .;
	@docker run --name drps-app --rm -d -p 8000:5000 drps-app;