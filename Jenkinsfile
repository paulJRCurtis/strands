pipeline {
    agent { label 'strands-docker-agent' }
    
    environment {
        DOCKER_IMAGE = "strands-security-platform"
        DOCKER_TAG = "${BUILD_NUMBER}"
        // DATADOG_API_KEY = credentials('datadog-api-key')
        
        // Environment-specific variables
        DEBUG = "${env.BRANCH_NAME == 'main' ? 'false' : 'true'}"
        LOG_LEVEL = "${env.BRANCH_NAME == 'main' ? 'INFO' : 'DEBUG'}"
        NODE_ENV = "${env.BRANCH_NAME == 'main' ? 'production' : 'development'}"
        API_BASE_URL = "http://coordinator:8000"
        FRONTEND_URL = "http://frontend:3000"
        CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000,http://frontend:3000"
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
                        sh 'npm install'
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
                    sh 'pytest tests/ --junitxml=test-results/test-results.xml --cov=src --cov-report=xml:test-results/coverage.xml'
                    
                    // Run frontend tests
                    dir('frontend') {
                        sh 'npm run test:coverage'
                        sh 'npm run lint'
                        sh 'npm run e2e'
                    }
                }
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'test-results/test-results.xml'
                    publishCoverage adapters: [coberturaAdapter('test-results/coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                    
                    // Publish frontend test results
                    dir('frontend') {
                        publishTestResults testResultsPattern: 'test-results/junit.xml'
                        publishCoverage adapters: [coberturaAdapter('test-results/coverage/cobertura-coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'test-results/playwright-report',
                            reportFiles: 'index.html',
                            reportName: 'Playwright E2E Report'
                        ])
                    }
                }
            }
        }
        stage('Code Quality') {
            steps {
                script {
                    echo 'Running code quality checks...'
                    
                    // SonarQube analysis
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            sonar-scanner \
                            -Dsonar.projectKey=strands-security-platform \
                            -Dsonar.sources=src,frontend/src \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info
                        '''
                    }
                    
                    // Quality gate check
                    timeout(time: 5, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
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
                stage('Container Security') {
                    steps {
                        script {
                            echo 'Scanning Docker image for vulnerabilities...'
                            // Trivy container scan for backend
                            sh "trivy image --format json --output trivy-backend-report.json ${DOCKER_IMAGE}-backend:${DOCKER_TAG}"
                            // Trivy container scan for frontend
                            sh "trivy image --format json --output trivy-frontend-report.json ${DOCKER_IMAGE}-frontend:${DOCKER_TAG}"
                        }
                    }
                }
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
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    echo 'Deploying application...'
                    // Push backend and frontend Docker images to registry
                    withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${DOCKER_IMAGE}-backend:${DOCKER_TAG}"
                        sh "docker push ${DOCKER_IMAGE}-backend:latest"
                        sh "docker push ${DOCKER_IMAGE}-frontend:${DOCKER_TAG}"
                        sh "docker push ${DOCKER_IMAGE}-frontend:latest"
                    }
                    // Deploy to test environment
                    echo 'Deploying to containerized test environment...'
                    try {
                        sh 'docker-compose -f docker-compose.test.yml run --rm test-coordinator'
                    } catch (Exception e) {
                        echo 'Backend tests failed - check test results for details'
                        sh 'docker-compose -f docker-compose.test.yml logs test-coordinator || true'
                        throw e
                    }
                    try {
                        sh 'docker-compose -f docker-compose.test.yml run --rm test-frontend'
                    } catch (Exception e) {
                        echo 'Frontend tests failed - check test results for details'
                        sh 'docker-compose -f docker-compose.test.yml logs test-frontend || true'
                        throw e
                    }
                    try {
                        sh 'docker-compose -f docker-compose.test.yml run --rm e2e-tests'
                    } catch (Exception e) {
                        echo 'E2E tests failed - check test results for details'
                        sh 'docker-compose -f docker-compose.test.yml logs e2e-tests || true'
                        throw e
                    }
                    // Deploy based on branch
                    if (env.BRANCH_NAME == 'develop') {
                        echo 'Deploying to staging environment...'
                        sh 'docker-compose -f docker-compose.dev.yml up -d'
                    } else if (env.BRANCH_NAME == 'main') {
                        echo 'Deploying to production environment...'
                        sh 'docker-compose -f docker-compose.prod.yml up -d'
                    }
                }
            }
            post {
                always {
                    // Archive containerized test results
                    archiveArtifacts artifacts: 'test-results/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'frontend/test-results/**/*', allowEmptyArchive: true
                    // Clean up test containers
                    sh 'docker-compose -f docker-compose.test.yml down || true'
                }
            }
        }
        stage('Health Check') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    echo 'Performing health checks...'
                    
                    sh '''
                        # Wait for containers to be ready
                        sleep 30
                        
                        # Health check for backend
                        curl -f http://localhost:8000/health || exit 1
                        
                        # Health check for frontend
                        curl -f http://localhost:3000 || exit 1
                    '''
                }
            }
        }
        
        stage('Monitoring & Alerting') {
            steps {
                script {
                    echo 'Setting up monitoring and alerting...'
                    
                    // Send deployment event to Datadog
                    sh '''
                        curl -X POST "https://api.datadoghq.com/api/v1/events" \
                        -H "Content-Type: application/json" \
                        -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                        -d '{
                            "title": "Strands Security Platform Deployment",
                            "text": "Build ${BUILD_NUMBER} deployed successfully",
                            "tags": ["environment:production", "service:strands", "version:${BUILD_NUMBER}"],
                            "alert_type": "success"
                        }'
                    '''
                    
                    // Health check and synthetic monitoring
                    sh '''
                        # Wait for application to be ready
                        sleep 30
                        
                        # Health check
                        curl -f http://localhost:8000/health || exit 1
                        
                        # Create Datadog synthetic test
                        curl -X POST "https://api.datadoghq.com/api/v1/synthetics/tests" \
                        -H "Content-Type: application/json" \
                        -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                        -d '{
                            "type": "api",
                            "subtype": "http",
                            "name": "Strands API Health Check",
                            "message": "API health check for Strands Security Platform",
                            "tags": ["service:strands", "environment:production"],
                            "config": {
                                "request": {
                                    "method": "GET",
                                    "url": "http://localhost:8000/health"
                                },
                                "assertions": [
                                    {
                                        "type": "statusCode",
                                        "operator": "is",
                                        "target": 200
                                    }
                                ]
                            },
                            "locations": ["aws:us-east-1"],
                            "options": {
                                "tick_every": 300
                            }
                        }'
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker images
            sh "docker rmi ${DOCKER_IMAGE}-backend:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}-backend:latest || true"
            sh "docker rmi ${DOCKER_IMAGE}-frontend:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}-frontend:latest || true"
            // Archive artifacts
            archiveArtifacts artifacts: '**/*-report.json, test-results/test-results.xml, test-results/coverage.xml', allowEmptyArchive: true
        }
        
        success {
            // Send success notification to Datadog
            echo "Pipeline succeeded"
            // sh '''
            //     curl -X POST "https://api.datadoghq.com/api/v1/events" \
            //     -H "Content-Type: application/json" \
            //     -H "DD-API-KEY: ${DATADOG_API_KEY}" \
            //     -d '{
            //         "title": "Pipeline Success",
            //         "text": "Strands Security Platform pipeline completed successfully",
            //         "tags": ["pipeline:jenkins", "status:success", "build:${BUILD_NUMBER}"],
            //         "alert_type": "success"
            //     }'
            // '''
        }
        
        failure {
            // Send failure notification to Datadog
            echo "Pipeline failed"
            // sh '''
            //     curl -X POST "https://api.datadoghq.com/api/v1/events" \
            //     -H "Content-Type: application/json" \
            //     -H "DD-API-KEY: ${DATADOG_API_KEY}" \
            //     -d '{
            //         "title": "Pipeline Failure",
            //         "text": "Strands Security Platform pipeline failed at build ${BUILD_NUMBER}",
            //         "tags": ["pipeline:jenkins", "status:failure", "build:${BUILD_NUMBER}"],
            //         "alert_type": "error"
            //     }'
            // '''
        }
    }
}