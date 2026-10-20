
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
                bat '"C:\Users\SALONI PEDNEKAR\AppData\Local\Programs\Python\Python312\python.exe"
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Users\\SALONI PEDNEKAR\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pytest -v'
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
