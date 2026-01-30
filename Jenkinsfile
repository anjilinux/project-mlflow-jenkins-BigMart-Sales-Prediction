pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "stock7"
    }

    stages {

        /* ================================
           Stage 1: Code Checkout
        ================================= */
        stage("Checkout Code") {
            steps {
                git branch: "master",
                    url: "https://github.com/anjilinux/project-mlflow-jenkins-BigMart-Sales-Prediction.git"
            }
        }

        /* ===  =============================
           Stage 2: Python Virtual Environment
        ================================= */
        stage("Setup Virtual Environment") {
            steps {
                sh '''
                python3 -m venv $VENV_NAME
                . $VENV_NAME/bin/activate

                pip install -r requirements.txt
                '''
                sh 'ls -R'
            }
        }

        /* ================================
           Stage 3: Data Ingestion
           data_ingestion.py
        ================================= */
        stage("Data Ingestion") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python data_ingestion.py
                '''
            }
        }

        /* ================================
           Stage 4: EDA & Feature Engineering
           eda_feature_engineering.py
        ================================= */
        stage("EDA & Feature Engineering") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python eda_feature_engineering.py
                '''
            }
        }

        /* ================================
           Stage 5: Data Preprocessing
           preprocessing.py
        ================================= */
        stage("Data Preprocessing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python preprocessing.py
                '''
            }
        }

        /* ================================
           Stage 6: Model Training (MLflow)
           train.py
        ================================= */
        stage("Model Training") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python train.py
                '''
            }
        }

        /* ================================
           Stage 7: Model Evaluation
           evaluate.py
        ================================= */
        stage("Model Evaluation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python evaluate.py
                '''
            }
        }

        /* ================================
           Stage 8: Model Testing (pytest)
        ================================= */
        stage("Model Testing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                pytest test_model.py  
                '''
            }
        }

        /* ================================
           Stage 9: Prediction Smoke Test
           predict.py
        ================================= */
        stage("Prediction Test") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python predict.py
                '''
            }
        }

        stage("DEPLOY-TO flask") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python app.py
                '''
            }
        }
        /* ================================
           Stage 10: Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '*.pkl', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ BigMart MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Logs"
        }
        // always {
        //     cleanWs()
        // }
    }
}
