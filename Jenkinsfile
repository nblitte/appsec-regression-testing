pipeline {
  agent any

  environment {
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
        sh '''
          if ! command -v newman >/dev/null 2>&1; then
            npm i -g newman
          fi
          # Reporter HTML pour Newman
          npm i -g newman-reporter-htmlextra
        '''
        // config/env.json n'est pas versionné : on le crée depuis l'exemple.
        // En usage réel, injecter identifiants/base_url via les credentials Jenkins.
        sh 'cp -n config/env.example.json config/env.json || true'
      }
    }

    stage('Web security regression (Selenium)') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p reports
          pytest --junitxml=reports/pytest-junit.xml \
                 --html=reports/pytest-report.html --self-contained-html
        '''
      }
    }

    stage('API security regression (Newman + tokens)') {
      steps {
        sh '''
          . .venv/bin/activate
          python api/get_tokens.py
          bash api/run_newman_v2.sh
        '''
      }
    }

    stage('Summary') {
      steps {
        sh '''
          . .venv/bin/activate
          python scripts/generate_summary_md.py
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/*.xml'
      archiveArtifacts artifacts: 'reports/**', fingerprint: true, allowEmptyArchive: true
    }
  }
}
