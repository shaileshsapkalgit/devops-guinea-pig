package com.shailesh.devops_guinea_pig.controller;

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

}
