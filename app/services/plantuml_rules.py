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
1. ARCHITECTURE & LAYOUT:
   - MUST use 'left to right direction' for logical Actor → System flow
   - MUST use 'skinparam linetype ortho' to avoid diagonal line clutter
   - Actors MUST be positioned outside the system boundary (left or right side)
   - Left side: Primary actors (who initiate actions)
   - Right side: Secondary actors (external systems, services)
2. SYSTEM BOUNDARY:
   - All use cases MUST be contained within 'rectangle "System Name" { ... }'
   - This defines the application boundary vs. external actors
   - Use cases are INSIDE, actors are OUTSIDE
3. ACTOR POSITIONING & ATTRIBUTES:
   - PRIMARY ACTORS: Define on the LEFT side using 'actor "Name" as ID'
   - SECONDARY ACTORS: Define on the RIGHT side (e.g., Payment Gateway, Email Service)
   - ACTOR ATTRIBUTES:
     * Create 'package "[Actor] Attributes"' positioned near the actor
     * Inside package, define attributes as 'usecase (attributeName) <<Attribute>>'
     * Connect attributes to their actor using dashed line: 'actor -- (attribute)'
   - ALL attributes MUST be related/connected to their respective actors
   - Attributes represent actor properties (e.g., username, email, role)
4. FUNCTIONAL DEPTH:
   - Each primary actor MUST have at least 4 associated use cases
   - This ensures complete workflow representation
   - Use meaningful, action-oriented use case names
5. BEHAVIORAL RELATIONSHIPS (<<include>> and <<extend>>):
   - <<include>>: Mandatory sub-processes
     * Syntax: '(BaseUC) ..> (RequiredUC) : <<include>>'
     * Example: (Checkout) ..> (Validate Payment) : <<include>>
     * Use when base UC ALWAYS needs the included UC
   - <<extend>>: Optional/conditional processes
     * Syntax: '(ExtendingUC) ..> (BaseUC) : <<extend>>'
     * Example: (Apply Discount) ..> (Checkout) : <<extend>>
     * Use for optional features or conditional paths
   - RULE: Every include/extend MUST be logically justified and connected to actor workflows
6. ACTOR-TO-USECASE ASSOCIATIONS:
   - MANDATORY: Every use case MUST be associated with at least one actor
   - Syntax: 'actor --> (UseCase)' for primary initiation
   - Syntax: '(UseCase) --> actor' for secondary actor involvement
   - ALL use cases must trace back to an actor interaction
7. GENERALIZATION (Inheritance):
   - Actor inheritance: 'ParentActor <|-- ChildActor'
   - Use case inheritance: 'ParentUC <|-- ChildUC'
   - Example: 'User <|-- Admin' (Admin is a specialized User)
   - Use for "is-a" relationships only
8. VISUAL STYLING (MANDATORY):
   skinparam usecase {
     BackgroundColor White
     BorderColor Black
     ' Attribute distinction
     BackgroundColor<<Attribute>> #F8F9FA
     BorderColor<<Attribute>> #ADB5BD
     FontSize<<Attribute>> 10
   }
   skinparam package {
     BackgroundColor #E8EAF6
     BorderColor #5C6BC0
     FontStyle bold
   }
   skinparam actor {
     BackgroundColor #BBDEFB
     BorderColor #1976D2
   }
   skinparam ArrowColor #263238
9. ATTRIBUTE-ACTOR RELATIONSHIP RULES:
   - Attributes MUST be grouped in packages labeled "[ActorName] Attributes"
   - Each attribute MUST have <<Attribute>> stereotype
   - Connection: 'ActorID -- (attributeID)' using dashed line
   - Attributes are NOT use cases but data properties of actors
   - Position attribute packages adjacent to their actors (left for left actors, right for right actors)
10. COMPLETENESS CHECKLIST:
    ✓ All actors positioned left (primary) or right (secondary)
    ✓ All actors have attribute packages with connections
    ✓ All use cases inside system boundary
    ✓ Every use case connected to at least one actor
    ✓ At least one <<include>> or <<extend>> relationship present
    ✓ Minimum 4 use cases per primary actor
    ✓ All attributes connected to their respective actors
    ✓ Proper stereotypes used (<<Attribute>>, <<include>>, <<extend>>)
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
1. HEADER: Use 'flowchart TD'.
2. ENTITY SHAPES:
    - STRONG ENTITY: Independent entity. Define as 'NodeID[**Entity Name**]'.
    - WEAK ENTITY: Dependent entity (Composition nature). Define as 'WeakNodeID[[Entity Name]]'.
3. PRIMARY KEY NOTATION: 
    - ONLY the Primary Key attribute gets the combining underline character (U+0332: ̲ ).
    - Format: PK_NodeID([a̲t̲t̲r̲i̲b̲u̲t̲e̲N̲a̲m̲e̲])
4. ATTRIBUTE SHAPES:
    - REGULAR ATTRIBUTE: Standard stadium: 'Attr_NodeID([attributeName])'.
    - FOREIGN KEY ATTRIBUTE: Stadium with 'FK: ' prefix: 'FK_NodeID([FK: attributeName])'.
5. CLEAN LABELS: No 'PK:' inside parentheses. Use only 'FK: ' for foreign keys.
6. RELATIONSHIP SHAPES:
    - STRONG RELATIONSHIP: Single diamond: 'RelID{"Action Name"}'.
    - WEAK (IDENTIFYING) RELATIONSHIP: Double diamond: 'WeakRelID{{"Action Name"}}'.
7. CARDINALITY NOTATION:
    - Format: 'EntityA ---|1| RelID ---|M| EntityB'.
8. ATTRIBUTE CONNECTION RULE: 
    - Some attributes are missing and the lines for that attributes are still existing in the diagram.Identify and place the attributes in there place.
    - Link every attribute to its parent: 'NodeID --- Attr_NodeID'.
9. PROFESSIONAL STYLING (THE COLOR FIX):
    - Apply all styles at the VERY BOTTOM of the diagram.
    - STRONG ENTITIES (Blue): 'style NodeID fill:#e1f5fe,stroke:#01579b,stroke-width:2px'
    - WEAK ENTITIES (Pink): 'style WeakNodeID fill:#fce4ec,stroke:#880e4f,stroke-width:4px,color:#000'
    - ALL ATTRIBUTES (Gray): 'style AttrID fill:#f5f5f5,stroke:#616161,stroke-width:1px'
    - STRONG RELATIONSHIPS (Green): 'style RelID fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px'
    - WEAK RELATIONSHIPS (Yellow): 'style WeakRelID fill:#fff9c4,stroke:#fbc02d,stroke-width:4px'
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
