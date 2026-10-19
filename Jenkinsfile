pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        booleanParam(name: 'UPDATE_GITOPS', defaultValue: false,
                     description: 'Update image tag in helm values.yaml and push to main (Argo CD will deploy)')
    }

    tools {
        maven 'maven-3.9'
    }

    environment {
        DOCKERHUB_REPOSITORY = 'java1829/devops-guinea-pig'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.SHORT_SHA = sh(script: 'git rev-parse --short=7 HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "jenkins-${env.SHORT_SHA}-${env.BUILD_NUMBER}"
                }
                echo "Image tag will be: ${env.IMAGE_TAG}"
            }
        }

        stage('Build') {
            steps {
                sh 'mvn -B clean package -DskipTests'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'mvn -B test'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $DOCKERHUB_REPOSITORY:$IMAGE_TAG .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push $DOCKERHUB_REPOSITORY:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Update GitOps Tag') {
            when { expression { params.UPDATE_GITOPS } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-token',
                                                  usernameVariable: 'GH_USER',
                                                  passwordVariable: 'GH_TOKEN')]) {
                    sh '''
                        set -e
                        git config user.name "jenkins-bot"
                        git config user.email "jenkins-bot@users.noreply.github.com"
                        git fetch origin main
                        git checkout -B main origin/main
                        sed -i "0,/^  tag: /s|^  tag: .*|  tag: \\"$IMAGE_TAG\\"|" helm/devops-guinea-pig/values.yaml
                        git diff --stat
                        git add helm/devops-guinea-pig/values.yaml
                        git commit -m "Update image tag to $IMAGE_TAG [skip ci]"
                        git push "https://${GH_USER}:${GH_TOKEN}@github.com/shaileshsapkalgit/devops-guinea-pig.git" main
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success { echo "Done: ${env.DOCKERHUB_REPOSITORY}:${env.IMAGE_TAG}" }
        failure { echo 'Build failed. Check the stage logs above.' }
    }
}