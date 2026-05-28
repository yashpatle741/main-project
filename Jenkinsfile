pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'yashpatle99'
    }

    stages {

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Push Backend Image') {
            steps {
                sh 'docker push $DOCKERHUB_USERNAME/skillpulse-backend:latest'
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh 'docker push $DOCKERHUB_USERNAME/skillpulse-frontend:latest'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

    }
}