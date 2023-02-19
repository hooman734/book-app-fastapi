job("Docker Hub - fastapi") {
    container(displayName = "docker", image = "docker:latest") {
        shellScript {
          	env["USER"] = "hooman777"
          	env["PASS"] = "$Shima734kk"
            content = "docker login -u $USER -p $PASS"
        }

        service("docker:dind") {
            alias("dind")
          
        }
    }
}