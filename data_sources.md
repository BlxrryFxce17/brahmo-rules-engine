# Clinical Data Sources

The knowledge nodes and organizational hierarchies used to populate the BRAHMO Rules Engine database were modeled after real-world clinical guidelines and standard hospital structures to ensure the assessment scenarios are highly realistic.

## 1. Clinical Guidelines & Drug Interactions (Zone 2 - Global Nodes)
The global safety constraints injected during the Zone 2 phase were sourced from standard medical references:

*   **Warfarin + NSAID Interaction Constraint:** Sourced from standard pharmacological databases (e.g., Medscape Drug Interaction Checker, Drugs.com). Used to demonstrate how a critical, cross-departmental safety rule overrides a specific departmental pathway.
*   **Sepsis Protocol (v1 vs v2):** Modeled after the *Surviving Sepsis Campaign (SSC)* guidelines. Used to demonstrate the Temporal Filtering check (Check 4) where `SUPERSEDED` protocols are successfully filtered out to prevent the use of outdated medical instructions.

## 2. Departmental Clinical Facts (Zone 1 - Orthopedics & Cardiology)
The specific medical facts associated with the `ortho` and `cardiology` departments were synthetically generated based on standard medical textbooks to test the Isolation (Check 1) and Derivability (Check 5) filters:

*   **Orthopedics (e.g., "Paracetamol is an analgesic", "Osteoarthritis management"):** Basic definitions were assigned high derivability scores (>0.7) to ensure they are successfully stripped out by Check 5, mimicking the process of saving LLM tokens by removing redundant foundational knowledge.
*   **Cardiology (e.g., "Post-MI care protocols"):** Used strictly to verify the Isolation Check (Check 1). A user mapped to the Orthopedics department (Nurse Priya) successfully filters out all Cardiology nodes.

## 3. Organizational Hierarchy & Compliance Tags
*   **Hierarchy Levels:** Modeled after a standard tier-based hospital organizational chart (Tiers 1-10), spanning from general administration (Tier 1) up to specialized Chief Medical Officers / HODs (Tier 10).
*   **Compliance Tags:** Security tags such as `MNPI` (Material Non-Public Information) and `CONFIDENTIAL` are standard data-governance classifications used in enterprise compliance frameworks (e.g., HIPAA, SOC2) to restrict sensitive nodes during Check 2.
