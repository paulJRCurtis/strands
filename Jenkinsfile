pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "strands-security-platform"
        DOCKER_TAG = "${BUILD_NUMBER}"
        OCTOPUS_PROJECT = "SecurityAnalysisPlatform"
        DATADOG_API_KEY = credentials('datadog-api-key')
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building application artifacts...'
                    
                    // Install Python dependencies
                    sh 'pip install -r requirements.txt'
                    
                    // Build frontend
                    dir('frontend') {
                        sh 'npm install'
                        sh 'npm run build'
                    }
                    
                    // Build Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    
                    // Install test dependencies
                    sh 'pip install -r requirements-dev.txt'
                    
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
                            echo 'Running SAST security scan...'
                            
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
                            
                            // Trivy container scan
                            sh "trivy image --format json --output trivy-report.json ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        }
                    }
                }
                stage('Dependency Check') {
                    steps {
                        script {
                            echo 'Checking dependencies for vulnerabilities...'
                            
                            // OWASP Dependency Check
                            sh 'dependency-check --project "Strands Security Platform" --scan . --format JSON --out dependency-check-report.json'
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
                    
                    // Push Docker image to registry
                    withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
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
                    
                    // Deploy to staging environment
                    if (env.BRANCH_NAME == 'develop') {
                        sh '''
                            kubectl set image deployment/strands-coordinator coordinator=${DOCKER_IMAGE}:${DOCKER_TAG} -n staging
                            kubectl set image deployment/strands-frontend frontend=${DOCKER_IMAGE}:${DOCKER_TAG} -n staging
                            kubectl rollout status deployment/strands-coordinator -n staging
                        '''
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
        
        stage('Release') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Creating Octopus Deploy release...'
                    
                    withCredentials([string(credentialsId: 'octopus-api-key', variable: 'OCTOPUS_API_KEY')]) {
                        sh '''
                            # Create Octopus release
                            octo create-release \
                                --project="${OCTOPUS_PROJECT}" \
                                --version="${BUILD_NUMBER}" \
                                --server="${OCTOPUS_SERVER}" \
                                --apiKey="${OCTOPUS_API_KEY}" \
                                --packageVersion="${DOCKER_TAG}" \
                                --releaseNotes="Build ${BUILD_NUMBER} - ${GIT_COMMIT}"
                            
                            # Deploy to production
                            octo deploy-release \
                                --project="${OCTOPUS_PROJECT}" \
                                --version="${BUILD_NUMBER}" \
                                --deployTo="Production" \
                                --server="${OCTOPUS_SERVER}" \
                                --apiKey="${OCTOPUS_API_KEY}" \
                                --waitForDeployment
                        '''
                    }
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
                        curl -f https://strands.company.com/health || exit 1
                        
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
                                    "url": "https://strands.company.com/health"
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
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}:latest || true"
            
            // Archive artifacts
            archiveArtifacts artifacts: '**/*-report.json, test-results/test-results.xml, test-results/coverage.xml', allowEmptyArchive: true
        }
        
        success {
            // Send success notification to Datadog
            sh '''
                curl -X POST "https://api.datadoghq.com/api/v1/events" \
                -H "Content-Type: application/json" \
                -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                -d '{
                    "title": "Pipeline Success",
                    "text": "Strands Security Platform pipeline completed successfully",
                    "tags": ["pipeline:jenkins", "status:success", "build:${BUILD_NUMBER}"],
                    "alert_type": "success"
                }'
            '''
        }
        
        failure {
            // Send failure notification to Datadog
            sh '''
                curl -X POST "https://api.datadoghq.com/api/v1/events" \
                -H "Content-Type: application/json" \
                -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                -d '{
                    "title": "Pipeline Failure",
                    "text": "Strands Security Platform pipeline failed at build ${BUILD_NUMBER}",
                    "tags": ["pipeline:jenkins", "status:failure", "build:${BUILD_NUMBER}"],
                    "alert_type": "error"
                }'
            '''
        }
    }
}