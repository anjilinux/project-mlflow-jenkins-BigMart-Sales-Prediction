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

stage("Prediction API Test") {
    steps {
        sh '''
        echo "Activating virtual environment..."
        . venv/bin/activate

        # Kill any process running on port 5001
        PORT=5001
        PID=$(lsof -ti:$PORT)
        if [ -n "$PID" ]; then
            echo "Port $PORT is in use by PID(s): $PID. Killing..."
            kill -9 $PID
            echo "Killed previous Flask process."
            sleep 2
        else
            echo "Port $PORT is free."
        fi

        # Export Flask app
        export FLASK_APP=app.py

        # Start Flask in background
        echo "Starting Flask API..."
        nohup python -m flask run --host=0.0.0.0 --port=$PORT > flask.log 2>&1 &
        FLASK_PID=$!
        echo "Flask PID: $FLASK_PID"

        # Wait for health endpoint
        echo "Waiting for Flask to be ready..."
        for i in {1..20}; do
            if curl -s -f http://localhost:$PORT/health > /dev/null; then
                echo "Flask is healthy!"
                break
            fi
            echo "Waiting 2 seconds..."
            sleep 2
        done

        if ! curl -s -f http://localhost:$PORT/health > /dev/null; then
            echo "ERROR: Flask did not start in time!"
            cat flask.log
            kill -9 $FLASK_PID || true
            exit 1
        fi

        # Send test prediction
        echo "Sending prediction request..."
        RESPONSE=$(curl -s -X POST http://localhost:$PORT/predict \
            -H "Content-Type: application/json" \
            -d '{"features": [1,2,3,4,5,6,7,8,9]}')
        echo "Prediction response: $RESPONSE"

        # Stop Flask
        echo "Stopping Flask..."
        kill -9 $FLASK_PID || true
        echo "Flask stopped successfully."
        '''
    }
}






        // stage('Run Flask App') {
        //     steps {
        //         sh '''
        //         . venv/bin/activate
        //         nohup python app.py > flask.log 2>&1 &
        //         sleep 5
        //         curl http://localhost:5001/
        //         '''
        //     }
        // }





        
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
