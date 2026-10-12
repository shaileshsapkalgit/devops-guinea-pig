package com.shailesh.devops_guinea_pig.controller;

import com.shailesh.devops_guinea_pig.Entity.Person;
import com.shailesh.devops_guinea_pig.Repository.PersonRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.web.bind.MethodArgumentNotValidException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/persons")
public class PersonController {

    private final PersonRepository repository;

    public PersonController(PersonRepository repository) {
        this.repository = repository;
    }

    // CREATE
    @PostMapping
    public ResponseEntity<?> create(@Valid @RequestBody Person person) {
        person.setId(null); // always insert as new
        if (repository.existsByEmail(person.getEmail())) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(Map.of("error", "Email already exists"));
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(repository.save(person));
    }

    // READ ALL
    @GetMapping
    public List<Person> getAll() {
        return repository.findAll();
    }

    // READ ONE
    @GetMapping("/{id}")
    public ResponseEntity<Person> getOne(@PathVariable Long id) {
        return repository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // UPDATE
    @PutMapping("/{id}")
    public ResponseEntity<?> update(@PathVariable Long id, @Valid @RequestBody Person updated) {
        return repository.findById(id).map(existing -> {
            if (repository.existsByEmailAndIdNot(updated.getEmail(), id)) {
                return ResponseEntity.status(HttpStatus.CONFLICT)
                        .body((Object) Map.of("error", "Email already exists"));
            }
            existing.setName(updated.getName());
            existing.setEmail(updated.getEmail());
            existing.setAge(updated.getAge());
            existing.setCity(updated.getCity());
            return ResponseEntity.ok((Object) repository.save(existing));
        }).orElse(ResponseEntity.notFound().build());
    }

    // DELETE
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!repository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        repository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // Validation errors -> {"name":"Name is required", ...}
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map<String, String> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors()
                .forEach(e -> errors.put(e.getField(), e.getDefaultMessage()));
        return errors;
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public Map<String, String> handleConflict() {
        return Map.of("error", "Email already exists");
    }
}

