pipeline {
    agent any

    stages {
        stage('安装依赖') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('运行 Python 脚本') {
            steps {
                sh '''
                    source venv/bin/activate
                    python convert_all.py testdemo.testproject-deep.xml
                '''
            }
        }
    }

    post {
        success {
            echo "✅ 转换完成"
            archiveArtifacts artifacts: '*.csv', fingerprint: true
        }
        failure {
            echo "❌ 失败了，请检查日志"
        }
    }
}
