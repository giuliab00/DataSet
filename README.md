# **Dataset Overview**
The dataset consists of user interactions categorized into **nine** different predicates representing various mental states. Each predicate is further divided into **explicit** and **implicit** levels, capturing different ways users express themselves. The dataset provides structured conversations between a child and a robot across different contexts.

---

## **Dataset Structure**
The dataset is stored in `all_data.json` and is structured as follows:

```json
{
  "predicate": {
    "level": [
      {
        "id": integer,
        "context": "string",
        "phrases": [
          "string",
          "string",
          ...
        ]
      }
    ]
  }
}
```

### **Key Components:**
1. **`predicate`**: Represents the emotional or behavioral state of the user. There are **nine** predicates in total:
   - **Hard**
   - **Easy**
   - **Bored**
   - **Tired**
   - **Hungry**
   - **Succeed**
   - **Fussy**
   - **Curious**
   - **Uncomfortable**

2. **`level`**: Specifies whether the interaction is **explicit** or **implicit**:
   - **Explicit**: The user directly states their feelings (e.g., "This is too hard!").
   - **Implicit**: The user indirectly expresses their feelings (e.g., "I’m not sure how to do this.").

3. **`id`**: A unique identifier for each interaction.
4. **`context`**: The scenario in which the interaction occurs (e.g., "Math Homework," "Playing a Game").
5. **`phrases`**: A list of dialogue exchanges between a child and a robot.
   - Each interaction contains **8 phrases**, but they can be easily sliced into **2, 4, or 6** at a time for different analytical approaches.

---

## **Usage Notes**
- The dataset can be **filtered** by predicate, level, or context to extract specific interactions.
- The phrase sets can be **sliced** into smaller groups (e.g., 2, 4, or 6 phrases) to analyze different interaction dynamics.
- The dataset can be **converted** into different formats (e.g., CSV, structured text) for further analysis.

---

This dataset provides a structured and versatile resource for understanding human-computer interactions and emotional states in various learning and engagement scenarios.
