drps:
	@deactivate;
	@source venv/bin/activate;
	@gunicorn -w 4 -b 0.0.0.0 'src.app:create_app()'
	