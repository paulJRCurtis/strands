#!/bin/bash
# Strands Jenkins Agent Verification Script
# This script verifies that all required tools are installed and working
# correctly in the Jenkins agent container.

set -e

echo "🔍 Verifying Strands Jenkins Agent Setup..."
echo "=============================================="

# Function to check command availability and version
check_tool() {
    local tool=$1
    local version_flag=${2:-"--version"}
    
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✅ $tool: $("$tool" "$version_flag" 2>&1 | head -n1)"
    else
        echo "❌ $tool: NOT FOUND"
        return 1
    fi
}

# Check Docker (requires socket mount)
echo "🐳 Checking Docker..."
if [ -S /var/run/docker.sock ]; then
    check_tool docker --version
    echo "   Docker socket: ✅ Available"
    
    # Test Docker functionality
    if docker ps >/dev/null 2>&1; then
        echo "   Docker functionality: ✅ Working"
    else
        echo "   Docker functionality: ❌ Not working (check permissions)"
    fi
else
    echo "   Docker socket: ❌ Not mounted"
fi

# Check Docker Compose
echo "🏗️  Checking Docker Compose..."
check_tool docker-compose --version

# Check Python and tools
echo "🐍 Checking Python environment..."
check_tool python3 --version
check_tool pip3 --version
check_tool pytest --version
check_tool bandit --version

# Check Node.js and npm
echo "📦 Checking Node.js environment..."
check_tool node --version
check_tool npm --version

# Check security tools
echo "🔒 Checking security tools..."
check_tool trivy --version

# Check SonarQube scanner
echo "📊 Checking code quality tools..."
check_tool sonar-scanner --version

# Check utility tools
echo "🛠️  Checking utility tools..."
check_tool curl --version
check_tool git --version
check_tool sed --version

# Check network connectivity (if Jenkins is running)
echo "🌐 Checking network connectivity..."
if [ -n "$JENKINS_URL" ]; then
    if curl -s --connect-timeout 5 "$JENKINS_URL" >/dev/null; then
        echo "   Jenkins connectivity: ✅ Accessible at $JENKINS_URL"
    else
        echo "   Jenkins connectivity: ⚠️  Cannot reach $JENKINS_URL"
    fi
else
    echo "   Jenkins connectivity: ⚠️  JENKINS_URL not set"
fi

# Check permissions
echo "🔐 Checking permissions..."
if groups | grep -q docker; then
    echo "   Docker group membership: ✅ jenkins user in docker group"
else
    echo "   Docker group membership: ❌ jenkins user not in docker group"
fi

# Check workspace
echo "📁 Checking workspace..."
if [ -w "/home/jenkins/agent" ]; then
    echo "   Workspace writable: ✅ /home/jenkins/agent"
else
    echo "   Workspace writable: ❌ /home/jenkins/agent not writable"
fi

# Summary
echo ""
echo "=============================================="
echo "🎯 Agent Verification Summary"
echo "=============================================="

# Count successful checks dynamically
critical_tools=("docker" "docker-compose" "python3" "node" "npm" "pytest" "bandit" "trivy" "sonar-scanner" "curl" "git" "sed")
total_checks=${#critical_tools[@]}
failed_checks=0

# Re-run critical checks for summary
for tool in "${critical_tools[@]}"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        ((failed_checks++))
    fi
done

successful_checks=$((total_checks - failed_checks))

echo "✅ Successful checks: $successful_checks/$total_checks"
if [ $failed_checks -eq 0 ]; then
    echo "🎉 All checks passed! Agent is ready for Strands pipeline."
    exit 0
else
    echo "❌ Failed checks: $failed_checks/$total_checks"
    echo "⚠️  Please fix the issues above before using this agent."
    exit 1
fi