pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'PlacementIQ project started'
            }
        }

        stage('Environment Setup') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Code Validation') {
            steps {
                bat 'python -m compileall -q .'
            }
        }

        stage('Automated Testing') {
            steps {
                bat 'python -m pytest tests -v'
            }
        }

        stage('Build') {
            steps {
                echo 'PlacementIQ build completed'
                archiveArtifacts artifacts: 'app.py,requirements.txt', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'PLACEMENTIQ PIPELINE SUCCESS!'
        }
        failure {
            echo 'PLACEMENTIQ PIPELINE FAILED!'
        }
    }
}