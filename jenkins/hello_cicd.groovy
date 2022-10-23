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
                script { build_stage = env.STAGE_NAME }
                dir('hellogene') {
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[ url: "https://github.com/ajayksri/hellogene"]]])
                }
            }
        }

        stage('Build') {
            steps {
                script { build_stage = env.STAGE_NAME }
                sh label: 'Build', script: '''
                pushd hellogene
                    ./build.sh
                popd
                '''
            }
        }

        stage('Deploy') {
            steps {
                script { build_stage = env.STAGE_NAME }
                sh label: 'Deploy', script: '''
                pushd hellogene
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

        stage('Cleanup') {
            steps {
                script { build_stage = env.STAGE_NAME }
                sh label: 'Build', script: '''
                pushd hellogene
                    ./jenkins/cleanup.sh
                popd
                '''
            }
        }
    }
}
