def path_env_file = ""

pipeline {
    agent any

    parameters {
        string(name: "container_name", defaultValue: "ensaware-api", description: "Nombre del contenedor de docker.")
        string(name: "image_name", defaultValue: "ensaware-api-img", description: "Nombre de la imagene docker.")
        string(name: "tag_image", defaultValue: "lts", description: "Tag de la imagen de la página.")
        string(name: "container_port", defaultValue: "8081", description: "Puerto que usa el contenedor")
    }

    stages {
        stage("Checkout") {
            steps {
                git branch: "main", url: "https://github.com/soyYaaG/ensaware-api.git"
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

                    try {
                        sh "docker stop ${container_name}"
                        sh "docker rm -f ${container_name}"
                        sh "docker rmi -f ${image_name}:${tag_image}"
                    } catch (Exception e) {
                        echo "Exception occurred: " + e.toString()
                    }
                    sh "docker build -t ${image_name}:${tag_image} ."
                }
            }
        }

        stage("Deploy") {
            steps {
                echo "${path_env_file}"
                script {
                    sh "docker run --env-file ${path_env_file}/.env -d -p ${container_port}:8081 --name ${container_name} ${image_name}:${tag_image}"
                }
            }
        }
    }
}
