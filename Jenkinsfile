pipeline {
    agent any

    stages {
        stage('Checkout') {
            step {
                git branch: 'main', url: 'https://github.com/soyYaaG/ensaware-api'
            }
        }

        stage('Build') {
            step {
                script {
                    try {
                        sh 'docker-compose build'
                        sh 'docker-compose up -d'
                    } catch (Exception e) {
                        echo 'Exception occurred: ' + e.toString()
                    }
                }
            }
        }

        stage('Deploy') {
            step {
                script {
                    try {
                        sh 'docker-compose up -d'
                    } catch (Exception e) {
                        echo 'Exception occurred: ' + e.toString()
                    }
                }
            }
        }
    }
}
