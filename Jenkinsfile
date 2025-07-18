pipeline {
    agent any

    environment {
        VENV = "venv"
        PATH = "${env.WORKSPACE}/${VENV}/bin:${env.PATH}"
    }

    stages {
        stage('准备环境') {
            steps {
                echo "创建 Python 虚拟环境并安装依赖"
                sh '''
                    python3 -m venv ${VENV}
                    source ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('运行转换脚本') {
            steps {
                echo "执行 convert_all.py 转换 XML 到 CSV"
                sh '''
                    source ${VENV}/bin/activate
                    python convert_all.py testdemo.testproject-deep.xml
                '''
            }
        }
    }

    post {
        success {
            echo "✅ 转换成功，归档 CSV 文件"
            archiveArtifacts artifacts: '*.csv', fingerprint: true
        }
        failure {
            echo "❌ 转换失败，请查看控制台日志"
        }
    }
}
