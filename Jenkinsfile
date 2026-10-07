// Skeleton pipeline. Assumes a Jenkins agent with Python 3 and network access to a running crAPI.
// TODO (you): point CRAPI_BASE_URL at your crAPI host and publish the HTML report.
pipeline {
    agent any
    environment {
        CRAPI_BASE_URL = 'http://localhost:8888'
    }
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml'
            }
        }
    }
    post {
        always {
            junit 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
