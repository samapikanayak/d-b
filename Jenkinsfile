  // *********************** Jenkins file for Development  server********************
pipeline {
  agent any
  environment{
	COMPOSE_FILE = "docker-compose.yml"
        }
	
stages {
  
  stage('Verify') {
            steps {
                sh '''
                    docker version
                    docker-compose version
                '''
            }
        }
		
		
    stage('clean') {
       steps {
         sh 'sh dockerclean.sh'
       }
    }

stage('Run Unit Test') {
steps {
    
      sh 'sh scan_python.sh'
      }
}
   

stage('Sonarqube scan') {
steps {
        script {
          scannerHome = tool 'sonar-scanner'
        }
        withSonarQubeEnv('sonarqube-server') {
          sh "${scannerHome}/bin/sonar-scanner -X"
        }
      }
}
    
	stage('Quality Gate') {
            steps {
			 withSonarQubeEnv('sonarqube-server') {
                waitForQualityGate abortPipeline: true
			}
            }
}
	
    stage('build') {
      steps {
        sh 'docker-compose build'
		
      }
    }
    
    stage('Deploy') {
      steps {
        sh 'docker-compose kill'
		sh 'docker-compose up -d'
      }
    }
  
}

}
