#!/bin/bash

# 🎨 Ansible Beautify - Quick Setup Script
# This script helps you get started with Ansible Beautify quickly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}🚀 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Welcome message
echo -e "${PURPLE}"
cat << "EOF"
  ____    _   _  ____ ___ ____  _     _____   ____  _____    _    _   _ _____ ___ _______   __
 / ___/  / \ | |/ ___|_ _| __ )| |   | ____| | __ )| ____|  / \  | | | |_   _|_ _|  ___\ \ / /
| |  _  / _ \| | |  _ | ||  _ \| |   |  _|   |  _ \|  _|   / _ \ | | | | | |  | || |_ _  \ V / 
| |_| |/ ___ \ | |_| || || |_) | |___| |___  | |_) | |___ / ___ \| |_| | | |  | ||  _|   | |  
 \____/_/   \_\|\____|___|____/|_____|_____| |____/|_____/_/   \_\\___/  |_| |___|_|     |_|  
                                                                                               
Transform your one-liner Ansible tasks into beautiful, readable YAML! 🎨
EOF
echo -e "${NC}"

# Check if running on supported OS
print_step "Checking system requirements..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_success "Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "macOS detected"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    print_success "Windows detected"
else
    print_warning "Unknown OS: $OSTYPE. Continuing anyway..."
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
print_step "Checking for required tools..."

# Check Docker
if command_exists docker; then
    print_success "Docker is installed"
    DOCKER_AVAILABLE=true
else
    print_warning "Docker not found. Manual installation will be required."
    DOCKER_AVAILABLE=false
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_success "Docker Compose is installed"
    DOCKER_COMPOSE_AVAILABLE=true
else
    print_warning "Docker Compose not found."
    DOCKER_COMPOSE_AVAILABLE=false
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js is installed ($NODE_VERSION)"
    NODE_AVAILABLE=true
else
    print_warning "Node.js not found."
    NODE_AVAILABLE=false
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 3 is installed ($PYTHON_VERSION)"
    PYTHON_AVAILABLE=true
elif command_exists python; then
    PYTHON_VERSION=$(python --version)
    print_success "Python is installed ($PYTHON_VERSION)"
    PYTHON_AVAILABLE=true
else
    print_warning "Python not found."
    PYTHON_AVAILABLE=false
fi

echo ""

# Setup options
print_step "Choose your setup method:"
echo "1. 🐳 Docker (Recommended - Easy and isolated)"
echo "2. 💻 Manual (Requires Node.js and Python)"
echo "3. 🔍 Just check requirements"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        if [ "$DOCKER_AVAILABLE" = true ] && [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
            print_step "Starting Docker setup..."
            
            # Stop any existing containers
            print_info "Stopping any existing containers..."
            docker-compose down 2>/dev/null || true
            
            # Build and start containers
            print_step "Building and starting containers..."
            docker-compose up -d --build
            
            # Wait a moment for containers to start
            sleep 5
            
            # Check if containers are running
            if docker-compose ps | grep -q "Up"; then
                print_success "Docker containers are running!"
                echo ""
                print_success "🎉 Ansible Beautify is ready!"
                print_info "Frontend: http://localhost:3000"
                print_info "Backend API: http://localhost:5000"
                echo ""
                print_info "To stop the application: docker-compose down"
                print_info "To view logs: docker-compose logs -f"
            else
                print_error "Failed to start containers. Check docker-compose logs for details."
                exit 1
            fi
        else
            print_error "Docker or Docker Compose not available. Please install them first."
            exit 1
        fi
        ;;
    2)
        if [ "$NODE_AVAILABLE" = true ] && [ "$PYTHON_AVAILABLE" = true ]; then
            print_step "Starting manual setup..."
            
            # Backend setup
            print_step "Setting up backend..."
            cd backend
            
            # Install Python dependencies
            if command_exists pip3; then
                pip3 install -r requirements.txt
            elif command_exists pip; then
                pip install -r requirements.txt
            else
                print_error "pip not found. Please install pip."
                exit 1
            fi
            
            print_success "Backend dependencies installed"
            
            # Start backend in background
            print_step "Starting backend server..."
            python3 api.py &
            BACKEND_PID=$!
            print_success "Backend started (PID: $BACKEND_PID)"
            
            # Frontend setup
            cd ../react-api
            print_step "Setting up frontend..."
            
            # Install Node dependencies
            npm install
            print_success "Frontend dependencies installed"
            
            # Start frontend
            print_step "Starting frontend server..."
            print_info "This will open a new terminal window/tab..."
            npm start &
            FRONTEND_PID=$!
            
            print_success "🎉 Manual setup complete!"
            echo ""
            print_info "Frontend: http://localhost:3000"
            print_info "Backend API: http://localhost:5000"
            echo ""
            print_warning "To stop the servers:"
            print_info "kill $BACKEND_PID (backend)"
            print_info "kill $FRONTEND_PID (frontend)"
            
        else
            print_error "Node.js and Python are required for manual setup."
            print_info "Please install:"
            [ "$NODE_AVAILABLE" = false ] && print_info "- Node.js: https://nodejs.org/"
            [ "$PYTHON_AVAILABLE" = false ] && print_info "- Python 3: https://www.python.org/"
            exit 1
        fi
        ;;
    3)
        print_step "System requirements check:"
        echo ""
        
        print_info "Required for Docker setup:"
        [ "$DOCKER_AVAILABLE" = true ] && echo "✅ Docker" || echo "❌ Docker"
        [ "$DOCKER_COMPOSE_AVAILABLE" = true ] && echo "✅ Docker Compose" || echo "❌ Docker Compose"
        
        echo ""
        print_info "Required for manual setup:"
        [ "$NODE_AVAILABLE" = true ] && echo "✅ Node.js" || echo "❌ Node.js"
        [ "$PYTHON_AVAILABLE" = true ] && echo "✅ Python" || echo "❌ Python"
        
        echo ""
        print_info "Installation links:"
        print_info "- Docker: https://docs.docker.com/get-docker/"
        print_info "- Node.js: https://nodejs.org/"
        print_info "- Python: https://www.python.org/"
        ;;
    *)
        print_error "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
print_success "Setup script completed! 🎉"
print_info "Need help? Check the README.md or open an issue on GitHub."
print_info "Repository: https://github.com/Courouge/ansible-beautify" 