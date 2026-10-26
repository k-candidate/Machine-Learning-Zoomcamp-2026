group "default" {
    targets = [
        "predict-churn"
    ]
}

target "predict-churn" {
    context = "."
    dockerfile = "Dockerfile"
    
    tags = [
        "docker.io/kcandidate/predict-churn:v1"
    ]
    output = [{type = "registry"}]
    
    platforms = [
        "linux/amd64",
        "linux/arm64"
    ]
    
    labels = {
        "org.opencontainers.image.title"       = "predict-churn-fastapi"
        "org.opencontainers.image.description" = "Image for predicting customer churn using a classification ML model"
    }
}