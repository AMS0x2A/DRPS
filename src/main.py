from src.app import create_app 
from src.data_instance import DataInstance


if __name__ == "__main__":
    create_app().run(host=DataInstance().host, port=DataInstance().port, debug=True)