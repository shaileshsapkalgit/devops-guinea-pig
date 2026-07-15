package com.shailesh.devops_guinea_pig.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HealthController {
    @GetMapping("/health")
    public Map<String,String> health(){

        return Map.of(
                "status","up",
                "application","devops-guinea-pig"
        );
    }
    @GetMapping("/")
    public Map<String, String> home() {
        return Map.of(
                "message", "Hello from hinjewadi...!!!",
                "version", "v2"
        );
    }
    @GetMapping("/hello")
    public Map<String, String> hello() {
        return Map.of(
                "message", "hello world",
                "version", "v10"
        );
    }
    @GetMapping("/bye")
    public Map<String, String> bye() {
        return Map.of(
                "message", "goodbye world",
                "version", "v8"
        );
    }

}
