---

# **JSON Dataset for Interaction Management**

## **Overview**
This dataset is designed to store and manage interactions for various predicates, levels of explicitness, contexts, and phrases. It is structured to support efficient retrieval, manipulation, and random access based on user-defined criteria.

---

## **File Structure**
The JSON file has the following hierarchical structure:

```json
{
  "predicates": {
    "predicate_name": {
      "level_of_explicitness": [
        {
          "id": integer,
          "context": "string",
          "phrases": [
            "string", 
            "string", 
            "string",
            ...
          ]
        },
        ...
      ]
    },
    ...
  }
}
```

### Key Components:
1. **`predicates`**: The top-level key containing all predicates (e.g., `"too hard"`, `"too easy"`, etc.).
2. **`predicate_name`**: A specific category or type of interaction.
3. **`level_of_explicitness`**: Three levels of explicitness are defined:
   - `"base"`: Fully explicit interactions.
   - `"no explicit word"`: Less direct interactions.
   - `"implicit"`: Indirect or subtle interactions.
4. **`id`**: A unique identifier for each interaction within the predicate and level.
5. **`context`**: Describes the situation or scenario the interaction relates to (e.g., `"math homework"`).
6. **`phrases`**: An array of strings representing the conversation flow.

---

## **Example Dataset**

Here’s an example of how the JSON file is structured:

```json
{
  "predicates": {
    "too hard": {
      "base": [
        {
          "id": 1,
          "context": "math homework",
          "phrases": [
            "This is too hard! I do not get it.",
            "Which problem is tricky? Lets check.",
            "This one. I cannot add these numbers.",
            "Okay, let start small. What is 300 plus 200?",
            "Um… 500?",
            "Great! Now, what is 40 plus 80?",
            "I do not know.",
            "Try again—think of it as 4 plus 8, then add a zero."
          ]
        }
      ]
    }
  }
}
```

---

## **Usage Instructions**

### **Loading the JSON File**
Use Python to load and work with the dataset:
```python
import json

with open("data.json", "r") as file:
    data = json.load(file)
```

### **Accessing Data**
- **Retrieve by Predicate and Level**:
  ```python
  data["predicates"]["too hard"]["base"]
  ```
- **Filter by Context**:
  ```python
  [i for i in data["predicates"]["too hard"]["base"] if i["context"] == "math homework"]
  ```
- **Access Specific Interaction**:
  ```python
  interaction = data["predicates"]["too hard"]["base"][0]
  ```

---

## **Data Retrieval Examples**

1. **Retrieve All Interactions for a Predicate**:
   ```python
   predicate_data = data["predicates"]["too hard"]
   ```

2. **Retrieve Specific Phrases**:
   ```python
   phrases = data["predicates"]["too hard"]["base"][0]["phrases"]
   first_four = phrases[:4]
   ```

3. **Retrieve Random Interaction**:
   ```python
   import random
   random_interaction = random.choice(data["predicates"]["too hard"]["base"])
   ```

4. **Filter by Context**:
   ```python
   context_filtered = [
       i for i in data["predicates"]["too hard"]["base"] 
       if i["context"] == "math homework"
   ]
   ```

---

## **Extending the Dataset**
### Adding a New Predicate:
To add a new predicate:
1. Define the predicate name under the `predicates` key.
2. Add levels of explicitness as subkeys (`base`, `no explicit word`, `implicit`).
3. Populate interactions under each level, with `id`, `context`, and `phrases`.

### Example:
```json
"new_predicate": {
  "base": [
    {
      "id": 1,
      "context": "example context",
      "phrases": ["Example phrase 1", "Example phrase 2"]
    }
  ]
}
```

---

## **Contact**
For questions or contributions, contact:
- **Name**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [Your GitHub Link](https://github.com/yourprofile)

---
