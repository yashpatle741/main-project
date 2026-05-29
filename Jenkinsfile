pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'yashpatle99'
        DB_USER = 'skillpulse'
        DB_NAME = 'skillpulse'
        DB_HOST = 'db'
        DB_PORT = '3306'
    }

    stages {

        stage('Create Env File') {
            steps {
                withCredentials([
                    string(credentialsId: 'MYSQL_ROOT_PASSWORD', variable: 'MYSQL_ROOT_PASSWORD'),
                    string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD')
                ]) {
                    sh '''
                    cat > .env << EOF
                    MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
                    DB_HOST=$DB_HOST
                    DB_PORT=$DB_PORT
                    DB_USER=$DB_USER
                    DB_PASSWORD=$DB_PASSWORD
                    DB_NAME=$DB_NAME
                    DOCKERHUB_USERNAME=$DOCKERHUB_USERNAME
                    EOF
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
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