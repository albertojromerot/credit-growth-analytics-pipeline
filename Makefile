.PHONY: install run test dashboard validate clean

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

run:
	python -m src.run_pipeline

test:
	python -m pytest tests -q

dashboard:
	python -m streamlit run dashboard/streamlit_app.py

validate: run test

clean:
	rm -rf .pytest_cache
	rm -rf **/__pycache__
