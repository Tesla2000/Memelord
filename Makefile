.PHONY: help setup setup-gather clean

help:
	@echo "Available commands:"
	@echo "  make setup          - Create virtual environment and install core dependencies"
	@echo "  make setup-gather - Create virtual environment and install core + gather dependencies"
	@echo "  make clean          - Remove virtual environment"
	@echo "  make help           - Show this help message"

setup:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing core dependencies..."
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"

setup-gather:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing core + gather dependencies..."
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements-gather.txt
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"

clean:
	@echo "Removing virtual environment..."
	rm -rf .venv
	@echo "Clean complete."
