# ==========================================
# Stage 1: Build Stage
# ==========================================
FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder

WORKDIR /app

# १. Dependency caching: pom.xml आधी कॉपी करून dependencies डाउनलोड करणे
# (यामुळे कोड बदलला तरी dependencies पुन्हा डाउनलोड होत नाहीत, वेळ वाचतो)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# २. Source code कॉपी करून Build करणे
COPY src ./src
RUN mvn clean package -DskipTests

# ==========================================
# Stage 2: Production-Ready Runtime Stage
# ==========================================
FROM eclipse-temurin:21-jre-alpine

# ३. Non-root user आणि group तयार करणे (Security साठी खूप महत्त्वाचे)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# ४. Builder स्टेजमधून फक्त JAR फाईल कॉपी करणे आणि तिची मालकी (ownership) non-root user ला देणे
COPY --from=builder --chown=appuser:appgroup /app/target/devops-guinea-pig-0.0.1-SNAPSHOT.jar app.jar

# ५. Root ऐवजी non-root user कडे स्विच करणे
USER appuser

EXPOSE 8080

# ६. ENTRYPOINT array format मध्ये देणे
# (हे Kubernetes मध्ये Pod terminate होताना SIGTERM सिग्नल व्यवस्थित हँडल करण्यासाठी गरजेचे असते)
ENTRYPOINT ["java", "-jar", "app.jar"]