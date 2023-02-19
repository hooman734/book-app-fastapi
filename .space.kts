job("Docker Hub - fastapi") {
    container(displayName = "docker", image = "docker:latest") {
        shellScript {
          	env["USER"] = Params("dockerhub-username")
          	env["PASS"] = Secrets("dockerhub-password")
            content = "docker login -u ${'$'}USER -p ${'$'}PASS
        }

        service("docker:dind") {
            alias("dind")
          
        }
    }
}