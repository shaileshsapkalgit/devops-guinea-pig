package com.shailesh.devops_guinea_pig.controller;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HelloDeepakController {

    @GetMapping("/hello-deepak")
    public Map<String, String> helloDeepak() {
        return Map.of(
                "message", "Hello Deepak!",
                "version", "v1"
        );
    }
    @GetMapping(value = "/git", produces = MediaType.TEXT_HTML_VALUE)
    public String helloGit() {
        return """
        <html>
          <body style="font-family: Arial;">
            <h1>Hello from git-practice branch!</h1>
            <p>Version: v1.0.1 <b>v2</b></p>
          </body>
        </html>
        """;
    }

}
