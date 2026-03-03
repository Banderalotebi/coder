#!/bin/bash
# Startup script for TechPartner AI Coder
# Run this on your EC2 server

# Navigate to the project directory
cd /home/ubuntu/coder/advanced-coding-expert

# Start the FastAPI server with PM2
pm2 start "python3 -m uvicorn phase4-agentic.api_server:app --port 8000 --host 0.0.0.0" --name ai-coder

# Save PM2 state
pm2 save

# Show status
pm2 status

