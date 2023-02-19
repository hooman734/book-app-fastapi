job("Publish to Docker Hub") {
    host("Build artifacts and a Docker image") {
        // assign project secrets to environment variables
        env["HUB_USER"] = Params("dockerhub-username")
        env["HUB_TOKEN"] = Secrets("dockerhub-password")

        shellScript {
            // login to Docker Hub
            content = """
                docker login --username ${'$'}HUB_USER --password "${'$'}HUB_TOKEN"
            """
        }

        dockerBuildPush {
            labels["vendor"] = "hesamian"
            tags {
                +"hooman777/fastapi:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
            }
        }
    }
}