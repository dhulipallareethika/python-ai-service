ERD_SPECIFIC_RULES = """
1. Use 'skinparam linetype ortho' and 'hide circle'.
2. Use 'entity "Entity Name" as alias {' for table structures.
3. Define fields INSIDE the brackets: '* **primary_key** : TYPE', 'field_name : TYPE'.
4. CRITICAL: Use a horizontal line '--' ONLY inside the curly braces to separate the primary key. 
5. NEVER place separators like '--' or '==' outside of the entity brackets '}'. 
6. Use Crow's Foot notation: ||--o{, }|--, etc.
"""

SEQUENCE_RULES = """
1. Use 'autonumber' at the start.
2. Define participants: 'participant "Name" as Alias'.
3. CRITICAL: Only use 'activate Alias' immediately AFTER an incoming message.
4. Use 'deactivate Alias' immediately after the return message '-->'.
5. Do not use 'activate' for static data storage descriptions or relationships.
6. Ensure every 'alt', 'loop', or 'group' block is strictly closed with 'end'.
"""

CLASS_RULES = """
1. Use 'class "Name" {' and define attributes first, then methods.
2. Use visibility markers: - (private), # (protected), + (public).
3. Use standard arrows: <|-- (Inheritance), *-- (Composition), o-- (Aggregation).
"""

USE_CASE_RULES = """
1. Use 'left to right direction'.
2. Wrap use cases in 'package "System Name" { ... }'.
3. Define actors: 'actor :Actor Name: as Alias'.
4. COMPULSORY: Provide at least 4 use cases for each primary actor.
"""

COMPONENT_RULES = """
1. Use 'skinparam componentStyle uml2'.
2. Define components ONLY as: 'component [Display Name] as Alias'. Use square brackets [].
3. CRITICAL: Components must NOT contain attributes, methods, fields, or visibility symbols (+, -, #).
4. Components must NOT use curly braces '{}' or class/ERD syntax.
5. Use ONLY architectural relationships between components (-->).
6. FORBIDDEN keywords: participant, actor, autonumber, activate, deactivate, entity, class.
7. The diagram must represent SYSTEM ARCHITECTURE, not behavior or interactions.
"""

DATABASE_CODE_RULES = """
Task: Convert the provided JSON classes into production-ready Database Schemas.
1. SOURCE OF TRUTH: Use the 'className', 'attributes', and 'relationships' from the provided JSON.
2. OUTPUT: Generate standard SQL DDL (CREATE TABLE) and MongoDB JSON Schema validation.
3. CONSTRAINTS: 
   - DO NOT use @startuml or @enduml.
   - DO NOT explain the code.
   - Use '### SQL' and '### NoSQL' headers.
   - For SQL: Include Foreign Keys based on the JSON relationships.
   - For NoSQL: Provide the db.createCollection() syntax with $jsonSchema.
"""

API_CONTRACT_RULES = """
Task: Create a high-quality OpenAPI 3.1.0 YAML contract.
1. FORMAT: RAW YAML ONLY.
2. STRUCTURE:
   - info: {title: "Generated API", version: "1.0.0"}
   - components/schemas: Map every JSON class to a schema.
   - paths: Generate standard CRUD paths (GET /students, POST /students, etc.) for each class.
3. CONSTRAINTS:
   - NEVER use markdown backticks (```).
   - NEVER use PlantUML tags (@startuml).
   - Start immediately with 'openapi: 3.1.0'.
"""