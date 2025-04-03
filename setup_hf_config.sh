#!/bin/bash
# Script to set up HF configuration for RunpodOllama

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Hugging Face configuration for RunpodOllama...${NC}"

# Check if src/.env exists and contains HF_TOKEN
SRC_ENV="../src/.env"
if [ -f "$SRC_ENV" ]; then
    # Extract HF_TOKEN from src/.env (macOS compatible)
    HF_TOKEN=$(grep "HF_TOKEN=" "$SRC_ENV" | cut -d'=' -f2)
    
    if [ -n "$HF_TOKEN" ]; then
        echo -e "${GREEN}HF_TOKEN found in $SRC_ENV${NC}"
        
        # Create or update .env file in current directory
        if [ -f ".env" ]; then
            # Check if HF_TOKEN already exists in .env
            if grep -q "HF_TOKEN=" ".env"; then
                # Update existing HF_TOKEN
                sed -i '' "s/HF_TOKEN=.*/HF_TOKEN=$HF_TOKEN/" ".env"
                echo -e "${GREEN}Updated HF_TOKEN in .env${NC}"
            else
                # Append HF_TOKEN to .env
                echo "HF_TOKEN=$HF_TOKEN" >> ".env"
                echo -e "${GREEN}Added HF_TOKEN to .env${NC}"
            fi
        else
            # Create new .env file
            echo "HF_TOKEN=$HF_TOKEN" > ".env"
            echo -e "${GREEN}Created .env with HF_TOKEN${NC}"
        fi
    else
        echo -e "${RED}HF_TOKEN not found in $SRC_ENV${NC}"
        exit 1
    fi
else
    echo -e "${RED}Source .env file not found at $SRC_ENV${NC}"
    exit 1
fi

# Make scripts executable
echo -e "${GREEN}Making scripts executable...${NC}"
chmod +x setup_hf_model.py
chmod +x hf_auth.py
chmod +x install_binary.sh
chmod +x fix_poetry_install.py

echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Run the binary installation if you haven't already: ${GREEN}./install_binary.sh${NC}"
echo -e "2. Activate the virtual environment: ${GREEN}source .venv/bin/activate${NC}"
echo -e "3. Run the setup script: ${GREEN}python setup_hf_model.py${NC}"
echo -e "   - This will create a RunPod endpoint for Llama-3.1-8B-Instruct"
echo -e "   - Follow the prompts to configure the GPU type on the RunPod dashboard"
echo -e "   - Start the proxy server when ready"
echo -e ""
echo -e "${GREEN}Setup complete!${NC}" 