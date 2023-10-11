pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/soyYaaG/ensaware-api'
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker image ls'
                    sh 'docker-compose --version'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            sh 'docker-compose down -v'
        }
    }
}
