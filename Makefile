.PHONY: help setup setup-gather clean setup-win setup-gather-win clean-win

help:
	@echo "Available commands:"
	@echo "  make setup          - Create virtual environment and install core dependencies (Linux)"
	@echo "  make setup-gather   - Create virtual environment and install core + gather dependencies (Linux)"
	@echo "  make clean          - Remove virtual environment (Linux)"
	@echo "  make setup-win      - Create virtual environment and install core dependencies (Windows)"
	@echo "  make setup-gather-win - Create virtual environment and install core + gather dependencies (Windows)"
	@echo "  make clean-win      - Remove virtual environment (Windows)"
	@echo "  make help           - Show this help message"

setup:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Activating virtual environment and installing core dependencies..."
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"

setup-gather:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Activating virtual environment and installing core + gather dependencies..."
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements-gather.txt
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"

clean:
	@echo "Removing virtual environment..."
	rm -rf .venv
	@echo "Clean complete."

setup-win:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing core dependencies..."
	cmd /c ".venv\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements.txt"
	@echo "Setup complete. Activate the virtual environment with: .venv\Scripts\activate"

setup-gather-win:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing core + gather dependencies..."
	cmd /c ".venv\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements-gather.txt"
	@echo "Setup complete. Activate the virtual environment with: .venv\Scripts\activate"

clean-win:
	@echo "Removing virtual environment..."
	rmdir /s /q .venv
	@echo "Clean complete."
