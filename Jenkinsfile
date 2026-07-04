// pipeline {
//     agent any

//     environment {
//         DOCKERHUB_USERNAME = 'yashpatle99'
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 git branch: 'main',
//                     url: 'https://github.com/yashpatle741/main-project.git'
//             }
//         }

//        stage('Build Images') {
//     parallel {

//         stage('Build Backend') {
//             steps {
//                 sh 'docker build -t skillpulse-backend ./backend'
//             }
//         }

//         stage('Build Frontend') {
//             steps {
//                 sh 'docker build -t skillpulse-frontend ./frontend'
//             }
//         }
//     }
// }
//         stage('Docker Login') {
//             steps {
//                 withCredentials([
//                     usernamePassword(
//                         credentialsId: 'dockerhub-creds',
//                         usernameVariable: 'DOCKER_USER',
//                         passwordVariable: 'DOCKER_PASS'
//                     )
//                 ]) {
//                     sh '''
//                     echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
//                     '''
//                 }
//             }
//         }

//     stage('Push Images') {
//     parallel {

//         stage('Push Backend') {
//             steps {
//                 sh """
//                 docker tag skillpulse-backend ${DOCKERHUB_USERNAME}/skillpulse-backend:${BUILD_NUMBER}
//                 docker push ${DOCKERHUB_USERNAME}/skillpulse-backend:${BUILD_NUMBER}
//                 """
//             }
//         }

//         stage('Push Frontend') {
//             steps {
//                 sh """
//                 docker tag skillpulse-frontend ${DOCKERHUB_USERNAME}/skillpulse-frontend:${BUILD_NUMBER}
//                 docker push ${DOCKERHUB_USERNAME}/skillpulse-frontend:${BUILD_NUMBER}
//                 """
//             }
//         }
//     }
// }
//         stage('Deploy Kubernetes Resources') {
//             steps {
//                 sh 'kubectl apply -R -f k8s/'
//             }
//         }

//         stage('Update Deployment Image') {
//             steps {
//                 sh """
//                 kubectl set image deployment/backend \
//                 backend=${DOCKERHUB_USERNAME}/skillpulse-backend:${BUILD_NUMBER} \
//                 -n skillpulse

//                 kubectl set image deployment/frontend \
//                 frontend=${DOCKERHUB_USERNAME}/skillpulse-frontend:${BUILD_NUMBER} \
//                 -n skillpulse
//                 """
//             }
//         }

//         stage('Verify Rollout') {
//             steps {
//                 sh 'kubectl rollout status deployment/backend -n skillpulse --timeout=120s'
//                 sh 'kubectl rollout status deployment/frontend -n skillpulse --timeout=120s'
//             }
//         }
//     }
// }



pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'yashpatle99'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yashpatle741/main-project.git'
            }
        }

       stage('Build Images') {
    parallel {

        stage('Build Backend') {
            steps {
                sh 'docker build -t skillpulse-backend ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t skillpulse-frontend ./frontend'
            }
        }
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

    stage('Push Images') {
    parallel {

        stage('Push Backend') {
            steps {
                sh """
                docker tag skillpulse-backend ${DOCKERHUB_USERNAME}/skillpulse-backend:${BUILD_NUMBER}
                docker push ${DOCKERHUB_USERNAME}/skillpulse-backend:${BUILD_NUMBER}
                """
            }
        }

        stage('Push Frontend') {
            steps {
                sh """
                docker tag skillpulse-frontend ${DOCKERHUB_USERNAME}/skillpulse-frontend:${BUILD_NUMBER}
                docker push ${DOCKERHUB_USERNAME}/skillpulse-frontend:${BUILD_NUMBER}
                """
            }
        }
    }
}

stage('Update GitOps Repository') {
    steps {
        sshagent(credentials: ['github-ssh']) {

            dir('gitops') {
                deleteDir()

                sh """
                    git clone git@github.com:yashpatle741/main-project-gitops.git .

                    sed -i 's|image: yashpatle99/skillpulse-backend:.*|image: yashpatle99/skillpulse-backend:${BUILD_NUMBER}|' k8s/backend/Deployment.yaml

                    sed -i 's|image: yashpatle99/skillpulse-frontend:.*|image: yashpatle99/skillpulse-frontend:${BUILD_NUMBER}|' k8s/frontend/Deployment.yaml

                    git config user.name "Jenkins"
                    git config user.email "jenkins@local"

                    git add .

                    git diff --cached --quiet || git commit -m "Update images to build ${BUILD_NUMBER}"

                    git push origin main
                """
            }

        }
    }
}
}