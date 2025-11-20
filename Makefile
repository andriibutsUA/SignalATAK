.PHONY: help setup verify run run-d stop logs clean lint

help:
	@echo "SignalATAK Makefile Commands:"
	@echo ""
	@echo "  make setup          - Initial setup: link Signal account (first time only)"
	@echo "  make run            - Run the bot (after setup)"
	@echo "  make run-d          - Run the bot in detached mode"
	@echo "  make stop           - Stop all services"
	@echo "  make logs           - View logs"
	@echo "  make clean          - Stop and remove all containers and volumes"
	@echo "  make lint           - Run code formatting and type checking"
	@echo ""
	@echo "Configuration:"
	@echo "  Edit envs/integration.env to configure ATAK_HOST and BOT_PHONE"
	@echo ""

setup:
	@echo "============================================================"
	@echo "Signal Account Linking Setup"
	@echo "============================================================"
	@echo ""
	@echo "1. Starting Signal API service..."
	@echo "2. Open your browser to:"
	@echo "   http://127.0.0.1:8080/v1/qrcodelink?device_name=signal-atak-bot"
	@echo ""
	@echo "3. In your Signal mobile app:"
	@echo "   - Open Settings → Linked Devices"
	@echo "   - Tap '+' or 'Link New Device'"
	@echo "   - Scan the QR code from the browser"
	@echo ""
	@echo "4. Press Ctrl+C when linking is complete"
	@echo "5. Run 'make verify' to confirm the link"
	@echo ""
	@echo "============================================================"
	MODE=normal docker compose up signal-api

run:
	docker compose up

run-d:
	docker compose up -d
	@echo "Services started in detached mode"
	@echo "Use 'make logs' to view logs or 'make stop' to stop services"

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v
	@echo "All containers and volumes removed"

lint:
	ruff format
	ruff check --fix --select I
	pyright
