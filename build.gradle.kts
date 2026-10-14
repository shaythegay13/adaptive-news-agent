plugins {
    kotlin("jvm") version "2.1.21"
    application
}

group = "com.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.eclipse.lmos:arc-agents:0.185.0")
    implementation("org.eclipse.lmos:arc-server:0.185.0")
    
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    // arc-agents 0.185.0 and arc-server 0.185.0 require JVM 21.
    jvmToolchain(21)
}

application {
    mainClass.set("MainKt")
}
