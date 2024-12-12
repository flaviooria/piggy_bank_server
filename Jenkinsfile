pipeline {
  agent {
    node {
      label 'dev'
    }

  }
  stages {
    stage('python version') {
      steps {
        sh 'python3 --version'
      }
    }

  }
  environment {
    PYTHONPATH = '.'
  }
}