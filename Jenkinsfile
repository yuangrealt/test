pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Clone') {
            steps {
                // 自动拉取 GitHub 代码（已由 Jenkins SCM 拉取就可省略）
                echo "代码已通过 SCM 拉取完毕"
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "设置虚拟环境并安装依赖"
                sh '''
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Script') {
            steps {
                echo "运行主脚本 convert_all.py"
                sh '''
                    source ${VENV_DIR}/bin/activate
                    python convert_all.py
                '''
            }
        }
    }

    post {
        success {
            echo "✅ 构建成功"
        }
        failure {
            echo "❌ 构建失败"
        }
    }
}
