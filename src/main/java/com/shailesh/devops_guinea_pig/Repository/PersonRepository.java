package com.shailesh.devops_guinea_pig.Repository;

import com.shailesh.devops_guinea_pig.Entity.Person;

import org.springframework.data.jpa.repository.JpaRepository;

public interface PersonRepository extends JpaRepository<Person, Long> {
    boolean existsByEmail(String email);
    boolean existsByEmailAndIdNot(String email, Long id);
}
