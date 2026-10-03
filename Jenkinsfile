pipeline {

    agent {
        label 'devops-sre-agent'
    }

    environment {
        IMAGE_NAME = "devops-sre-demo"
        IMAGE_TAG  = "1.0.5"
        REGISTRY   = "192.168.127.2:5000"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install -r app/requirements.txt
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    ./venv/bin/python -c "from app.app import app; print('Application import test: PASSED')"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        ./app
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    echo "=== Trivy Vulnerability Report ==="

                    trivy image \
                        --severity HIGH,CRITICAL \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Trivy Security Gate') {
            steps {
                sh '''
                    echo "=== Trivy CRITICAL Security Gate ==="

                    trivy image \
                        --severity CRITICAL \
                        --exit-code 1 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    echo "=== Tagging Image ==="

                    docker tag \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

                    echo "=== Pushing Image ==="

                    docker push \
                        ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }

        failure {
            echo 'CI pipeline failed. Check the failed stage.'
        }
    }
}
