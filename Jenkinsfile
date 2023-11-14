def path_env_file = ""

pipeline {
    agent any

    stages {
        stage("Checkout") {
            steps {
                git branch: "dev", url: "https://github.com/soyYaaG/ensaware-api.git"
            }
        }

        stage ("Environment") {
            steps {
                script {
                    sh "env > .env"
                    path_env_file = pwd()
                }
            }
        }

        stage("Build") {
            steps {
                script {
                    sh "docker-compose build"
                }
            }
        }

        stage("Deploy") {
            steps {
                sh "docker-compose --env-file ${path_env_file}/.env up -d"
            }
        }
    }
}
