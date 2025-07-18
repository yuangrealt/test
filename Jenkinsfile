pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/你的用户名/项目名.git'
    }

    stages {
        stage('Clone') {
            steps {
                git credentialsId: 'github-token', url: "${env.GIT_REPO}", branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo "构建项目中..."
                // sh 'mvn clean package' 或其他构建命令
            }
        }

        stage('Test') {
            steps {
                echo "执行测试..."
                // sh 'mvn test'
            }
        }
    }
}
