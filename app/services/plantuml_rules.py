ERD_SPECIFIC_RULES = """
1. Use 'skinparam linetype ortho' to ensure clean, 90-degree relationship lines.
2. Use 'hide circle' and 'hide methods' to remove class-style icons and empty method sections.
3. Use 'entity "Entity Name" as alias {' for table structures.
4. Define fields INSIDE the brackets:
   - Use '* **field_name**' for Primary Keys.
   - Use 'field_name' for regular columns.
5. CRITICAL: Use a horizontal line '--' ONLY inside the curly braces to separate the primary key from other attributes.
6. NEVER place separators like '--' or '==' outside of the entity brackets.
7. Use Crow's Foot notation exclusively: 
   - Zero or Many: }o--
   - One or Many: }|--
   - Exactly One: ||--
8. Label relationships with ' : ' to describe the action (e.g., 'User ||--o{ Order : places').
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
ERD_MERMAID_RULES = """
1. HEADER: Use 'flowchart TD' (Top-Down) to reduce horizontal line length and keep the layout compact.
2. ENTITY SHAPE: Define entities as rectangles with bold text: 'ID[**Entity Name**]'.
3. ATTRIBUTE SHAPE: Use stadium/oval shapes for attributes: 'AttrID([Attribute Name])'. 
   - Note: Use '([ ])' instead of '(( ))' to produce professional ovals.
4. RELATIONSHIP SHAPE: Use diamond shapes: 'RelID{Action}'.
5. COMPACT CONNECTIONS:
   - Use '---' (three dashes) for vertical connections to balance the diagram.
   - Group attributes physically close to their entities in the code to minimize line length.
6. PROFESSIONAL STYLING:
   - ENTITIES: 'style ID fill:#dcfce7,stroke:#166534,stroke-width:2px,color:#166534'
   - ATTRIBUTES: 'style AttrID fill:#ccfbf1,stroke:#0d9488,stroke-width:1px,color:#0d9488'
   - RELATIONSHIPS: 'style RelID fill:#ffedd5,stroke:#9a3412,stroke-width:2px,color:#9a3412'
7. FORBIDDEN: Do not use circular nodes '(( ))'. Use only ovals '([ ])'.
"""

SEQUENCE_MERMAID_RULES = """
1. Use the 'sequenceDiagram' header.
2. Use 'autonumber' on the second line to enable message numbering.
3. Define participants: 'participant Alias as Display Name'.
4. CRITICAL: Use 'activate Alias' immediately after an incoming message (->>) and 'deactivate Alias' after the return (-->>).
5. For return messages, use the dotted arrow: 'Alias-->>Alias: message'.
6. Logic blocks must be strictly closed: 'alt ... else ... end', 'opt ... end', or 'loop ... end'.
"""

CLASS_MERMAID_RULES = """
1. Use the 'classDiagram' header at the top.
2. Define class members inside curly braces: 'class Name { visibility type name }'.
3. Use visibility markers: 
   - '-' (private)
   - '#' (protected)
   - '+' (public)
   - '~' (package/internal).
4. For methods, use the format: 'visibility name(params) type'.
5. Use standard Mermaid relationship arrows:
   - Inheritance: <|--
   - Composition: *--
   - Aggregation: o--
   - Association: -->
   - Dependency: ..>
   - Realization: ..|>
6. Use cardinality labels with quotes: 'ClassA "1" --> "*" ClassB : contains'.
7. CRITICAL: Do not use 'skinparam' or 'hide circle' as these are PlantUML-specific.
"""

USE_CASE_MERMAID_RULES = """
1. Use 'flowchart LR' (Left-to-Right) to maximize horizontal space and readability.
2. SYSTEM BOUNDARY: You MUST wrap all use cases in a 'subgraph' labeled "Student Management System".
3. ACTOR DEFINITION: Define actors using the circle shape: 'ActorID((Actor Name))'.
   - Include Student, Instructor, and Administrator as separate nodes outside the subgraph.
4. USE CASE DEFINITION: Define use cases using the rounded-rectangle shape: 'UseCaseID([Use Case Name])'.
   - Include every action: Enroll in Course, View Grades, Pay Fees, Update Profile, etc.
5. STYLING: Add a style command at the end to increase node size: 'classDef default fill:#f9f,stroke:#333,stroke-width:2px;'.
6. RELATIONSHIPS: Connect actors to use cases using '---'.
7. FULL SCOPE: Do not omit any actors or use cases found in the requirements; the code must be comprehensive.
"""

COMPONENT_MERMAID_RULES = """
1. HEADER: Always start with 'flowchart TD'.
2. SYSTEM BOUNDARY: You MUST wrap all identified modules within a 'subgraph "System Architecture"'.
3. COMPONENT SYNTAX: 
   - Define all functional modules/components using square brackets: 'ID[Display Name]'.
   - If a component represents a database or storage, use cylindrical brackets: 'ID[(Display Name)]'.
4. NO INTERNAL DETAIL: Components MUST NOT contain attributes, methods, visibility markers (+, -, #), or curly braces {}.
5. RELATIONSHIP SYNTAX: Use strictly directed arrows with descriptive labels: 'ID_A -->|action_label| ID_B'.
6. LAYERING LOGIC:
   - Place high-level interfaces/users at the top.
   - Place core logic/services in the middle.
   - Place data storage/databases at the bottom.
7. GLOBAL STYLING: You MUST append the following lines at the very end of every code block to ensure the diagram is large and readable:
   'classDef comp fill:#ffffff,stroke:#333,stroke-width:2px,color:#000;'
   'class <<ALL_DEFINED_IDS>> comp'
8. FORBIDDEN: Do not use 'erDiagram', 'classDiagram', 'sequenceDiagram', or any code-level syntax.
"""