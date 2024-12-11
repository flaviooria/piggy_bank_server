pipeline {
  agent {
    node {
      label 'dev'
    }

  }
  stages {
    stage('python version') {
      steps {
        sh 'python --version'
      }
    }

  }
  environment {
    PYTHONPATH = '.'
  }
}