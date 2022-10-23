#!/usr/bin/env groovy
pipeline {
    agent {
        node {
            label 'centos-7.9.x-node'
        }
    }

    stages {

        stage('Checkout') {

            steps {
                cleanWs()
                script { build_stage = env.STAGE_NAME }
                dir('hellogene') {
                    checkout([$class: 'GitSCM', branches: [[name: 'v03']], userRemoteConfigs: [[ url: "https://github.com/ajayksri/hellogene"]]])
                }
            }
        }

        stage('Build_Deploy') {
            steps {
                script { build_stage = env.STAGE_NAME }
                sh label: 'Deploy', script: '''
                pushd hellogene
                    chmod +x *.sh
                    chmod +x jenkins/*.sh
                    ./jenkins/deploy.sh
		            ./run.sh
                popd
                '''
            }
        }

        stage('Test') {
            steps {
                script { build_stage = env.STAGE_NAME }
                sh label: 'Test', script: '''
                pushd hellogene
                    ./jenkins/run_tests.sh
                popd
                '''
            }
        }
    }
}
