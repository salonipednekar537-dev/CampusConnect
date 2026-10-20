
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -3.12 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'py -3.12 -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'CampusConnect CI pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
