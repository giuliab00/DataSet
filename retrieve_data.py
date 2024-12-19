import json
import random

class DataRetriever:
    def __init__(self, file_path, specific_level, max_interactions, max_sentences):
        # Load the JSON data from the specified file
        with open(file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.specific_level = specific_level
        self.max_interactions = max_interactions
        self.max_sentences = max_sentences

    def parser(self, interaction):
        # Parse the interaction into a list of dictionaries with roles and content
        l = []
        for i in interaction:
            d = {}
            if i.startswith('Child:'):
                d['role'] = 'user'
                d['content'] = i[7:].strip()
            elif i.startswith('Robot:'):
                d['role'] = 'assistant'
                d['content'] = i[7:].strip()
            l.append(d)
        return l
    
    def retrieve_interaction(self):
        results = []
        all_interactions = []

        # Iterate over all predicates in the data
        for predicate, levels in self.data["predicates"].items():
            # Check if the specific level exists
            if self.specific_level in levels:
                interactions = levels[self.specific_level]
                # Limit the number of interactions per predicate
                for interaction in interactions[:self.max_interactions]:
                    all_interactions.append((predicate, interaction))

        # Debugging print to check the collected interactions
        print(f"Collected {len(all_interactions)} interactions.")

        # Process the interactions
        for predicate, interaction in all_interactions:
            context = interaction["context"]
            # Limit the number of sentences
            phrases = interaction["phrases"][:self.max_sentences]
            parsed_phrases = self.parser(phrases)
            results.append({
                "predicate": predicate,
                "context": context,
                "phrases": parsed_phrases
            })

        # Print the results for debugging purposes
        print(f"Returning {len(results)} interactions.")
        return results
