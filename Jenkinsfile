pipeline {
    agent { label 'strands-docker-agent' }
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
    }
    environment {
        DOCKER_IMAGE = "strands-security-platform"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/paulJRCurtis/strands.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building application artifacts...'
                    
                    // Install Python dependencies
                    sh 'pip install -r requirements.txt --break-system-packages'
                    
                    // Build frontend
                    dir('frontend') {
                        // this should be removed --include=dev
                        sh 'npm install npm install --include=dev'
                        sh 'npm run build'
                    }
                    
                    // Build backend Docker image
                    sh "docker build -t ${DOCKER_IMAGE}-backend:${DOCKER_TAG} -f backend/Dockerfile ."
                    sh "docker tag ${DOCKER_IMAGE}-backend:${DOCKER_TAG} ${DOCKER_IMAGE}-backend:latest"

                    // Build frontend Docker image
                    sh "docker build -t ${DOCKER_IMAGE}-frontend:${DOCKER_TAG} -f frontend/Dockerfile frontend"
                    sh "docker tag ${DOCKER_IMAGE}-frontend:${DOCKER_TAG} ${DOCKER_IMAGE}-frontend:latest"
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    
                    // Install test dependencies
                    sh 'pip install -r requirements-dev.txt --break-system-packages'
                    // Run backend tests
                    sh 'coverage run -m pytest --junitxml=test-results.xml'
                    sh 'coverage xml -o coverage.xml'
                    
                    // Run frontend tests
                    dir('frontend') {
                        sh 'npm run test:coverage'
                        sh 'npm run lint'
                    }
                }
            }

            post {
                always {
                    echo 'Publishing test results and coverage reports...'
                    // Publish frontend test results
                    dir('frontend') {
                        junit 'test-results/junit.xml'
                        recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']])
                        // publishHTML([
                        //     allowMissing: false,
                        //     alwaysLinkToLastBuild: true,
                        //     keepAll: true,
                        //     reportDir: 'test-results/playwright-report',
                        //     reportFiles: 'index.html',
                        //     reportName: 'Playwright E2E Report'
                        // ])
                    }
                }
            }


        }

        stage('Code Quality') {
            steps {
                script {
                    echo 'Running code quality checks...'
                    
                    // // SonarQube analysis
                    // withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    //     sh 'sonar-scanner -Dsonar.organization=pauljrcurtis-1 -Dsonar.projectKey=paulJRCurtis_8.1CDevSecOps'
                    // }
                    
                    // // Quality gate check
                    // timeout(time: 5, unit: 'MINUTES') {
                    //     waitForQualityGate abortPipeline: true
                    // }
                }
            }
        }
        stage('Security') {
            parallel {
                stage('SAST Scan') {
                    steps {
                        script {
                            // Bandit for Python security
                            sh 'bandit -r src/ -f json -o bandit-report.json || true'
                            // npm audit for frontend
                            dir('frontend') {
                                sh 'npm audit --audit-level=moderate --json > npm-audit.json || true'
                                sh 'npx @axe-core/cli http://localhost:3000 --save axe-report.json || true'
                            }
                        }
                    }
                }
                // stage('Container Security') {
                //     steps {
                //         script {
                //             echo 'Scanning Docker image for vulnerabilities...'
                //             // Trivy container scan for backend
                //             sh "trivy image --format json --output trivy-backend-report.json ${DOCKER_IMAGE}-backend:${DOCKER_TAG}"
                //             // Trivy container scan for frontend
                //             sh "trivy image --format json --output trivy-frontend-report.json ${DOCKER_IMAGE}-frontend:${DOCKER_TAG}"
                //         }
                //     }
                // }
                stage('Dependency Check') {
                    steps {
                        script {
                            echo 'Checking dependencies for vulnerabilities...'
                            // OWASP Dependency Check
                            sh 'dependency-check --project \"Strands Security Platform\" --scan . --format JSON --out dependency-check-report.json'
                        }
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '*-report.json, frontend/axe-report.json', allowEmptyArchive: true
                }
            }
        }
        
    }
    post {
        always {
            // cleanWs()
            // Clean up Docker images
            // input message: 'Do you want to approve the cleanup of Docker images?', ok: 'Yes'
            sh "docker rmi ${DOCKER_IMAGE}-backend:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}-backend:latest || true"
            sh "docker rmi ${DOCKER_IMAGE}-frontend:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}-frontend:latest || true"
            // Archive artifacts
            archiveArtifacts artifacts: '**/*-report.json, test-results/test-results.xml, test-results/coverage.xml', allowEmptyArchive: true
        }
        success {
            echo 'Build and tests succeeded!'
        }
    }
}