from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from retrieve_data import DataRetriever
from predicate_grounder import OpenAImethods

# Set language
language = "en"

# Method to load interactions
def load_data(parameters):
    file_path = "data.json"
    retriever = DataRetriever(file_path, specific_level=parameters["level"], max_interactions=parameters["interaction"], max_sentences=parameters["sentence"])
    # result contains [ {predicate: "predicate", context: "context", phrases: [{role: "user", content: "content"}]}, ...]
    result = retriever.retrieve_interaction()
    return result

def elaborate_data_binary(data, gt):
    y_true = []
    y_pred = []
    interactions = []
    for i in data:
        if i["predicate"] == gt:
            y_true.append(1)
        else:
            y_true.append(0)
        
        # Send request to OpenAI with context and phrases
        context = i["context"]
        phrases = i["phrases"]
        openai_instance = OpenAImethods(language, phrases, context, gt)
        openai_instance.binary_request()
        
        if openai_instance.response == "yes":
            y_pred.append(1)
        else:
            y_pred.append(0)
        
        interactions.append(i)

    return y_true, y_pred, interactions

def binary_cm(y_true, y_pred, gt, level, sentence, interactions):
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    metrics = classification_report(y_true, y_pred)
    print("Metrics: ")
    print(metrics)

    # Identify mismatched interactions (true 1 labeled as 0 and true 0 labeled as 1)
    mismatches_true_1_as_0 = [(i, true, pred) for i, (true, pred) in enumerate(zip(y_true, y_pred)) if true == 1 and pred == 0]
    mismatches_true_0_as_1 = [(i, true, pred) for i, (true, pred) in enumerate(zip(y_true, y_pred)) if true == 0 and pred == 1]

    print("Mismatched interactions (true 1 labeled as 0):")
    for idx, true, pred in mismatches_true_1_as_0:
        print(f"Index: {idx}, True: {true}, Predicted: {pred}, Interaction: {interactions[idx]}")

    print("Mismatched interactions (true 0 labeled as 1):")
    for idx, true, pred in mismatches_true_0_as_1:
        print(f"Index: {idx}, True: {true}, Predicted: {pred}, Interaction: {interactions[idx]}")

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted 0', 'Predicted 1'], yticklabels=['Actual 0', 'Actual 1'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix {gt} level: {level} sentence: {sentence}')

    # Save the confusion matrix as a PNG file
    filename = f'Confusion_Matrix_{gt}_level_{level}_sentence_{sentence}.png'
    plt.savefig(filename)
    plt.show()

    # Save the metrics and mismatches to a log file
    log_filename = 'confusion_matrix_metrics.log'
    with open(log_filename, 'a') as log_file:
        log_file.write(f'Confusion Matrix {gt} level: {level} sentence: {sentence}\n')
        log_file.write(metrics)
        log_file.write('\nMismatched interactions (true 1 labeled as 0):\n')
        for idx, true, pred in mismatches_true_1_as_0:
            log_file.write(f"Index: {idx}, True: {true}, Predicted: {pred}, Interaction: {interactions[idx]}\n")
        log_file.write('\nMismatched interactions (true 0 labeled as 1):\n')
        for idx, true, pred in mismatches_true_0_as_1:
            log_file.write(f"Index: {idx}, True: {true}, Predicted: {pred}, Interaction: {interactions[idx]}\n")
        log_file.write('\n\n')

def elaborate_data_multiclass(data, gt_list):
    y_true = []
    y_pred = []
    interactions = []
    for i in data:
        if i["predicate"] in gt_list:
            y_true.append(gt_list.index(i["predicate"]))
        else:
            y_true.append(len(gt_list))  # Assuming the last class is for "other" or "unknown"
        
        # Send request to OpenAI with context and phrases
        context = i["context"]
        phrases = i["phrases"]
        openai_instance = OpenAImethods(language, phrases, context, gt_list = gt_list)
        openai_instance.three_class_request()
        
        if openai_instance.response in gt_list:
            y_pred.append(gt_list.index(openai_instance.response))
        else:
            y_pred.append(len(gt_list))  # Assuming the last class is for "other" or "unknown"
        
        interactions.append(i)

    return y_true, y_pred, interactions

def multiclass_cm(y_true, y_pred, gt_list, level, sentence, interactions):
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    metrics = classification_report(y_true, y_pred, target_names=gt_list + ["other"])
    print("Metrics: ")
    print(metrics)

    # Identify mismatched interactions
    mismatches = [(i, true, pred) for i, (true, pred) in enumerate(zip(y_true, y_pred)) if true != pred]
    print("Mismatched interactions:")
    for idx, true, pred in mismatches:
        print(f"Index: {idx}, True: {gt_list[true] if true < len(gt_list) else 'other'}, Predicted: {gt_list[pred] if pred < len(gt_list) else 'other'}, Interaction: {interactions[idx]}")

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=gt_list + ["other"], yticklabels=gt_list + ["other"])
    plt.xlabel('Predicted', fontsize=14)
    plt.ylabel('Actual', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    
    plt.title(f'Confusion Matrix level: {level} sentence: {sentence}')

    # Save the confusion matrix as a PNG file
    filename = f'Confusion_Matrix_3_level_{level}_sentence_{sentence}.png'
    plt.savefig(filename)
    plt.show()

    # Save the metrics and mismatches to a log file
    log_filename = 'confusion_matrix_3_metrics.log'
    with open(log_filename, 'a') as log_file:
        log_file.write(f'Confusion Matrix level: {level} sentence: {sentence}\n')
        log_file.write(metrics)
        log_file.write('\nMismatched interactions:\n')
        for idx, true, pred in mismatches:
            log_file.write(f"Index: {idx}, True: {gt_list[true] if true < len(gt_list) else 'other'}, Predicted: {gt_list[pred] if pred < len(gt_list) else 'other'}, Interaction: {interactions[idx]}\n")
        log_file.write('\n\n')


if __name__ == "__main__":

    # Example usage for debugging
    parameter = {"level": "intermediate", "sentence": 8, "interaction": 50}
    predicate_list_bi = ["the user feels bored","the user feels tired","the user is hungry","the user is fussy about the task details","the user wants to succeed in the task"]
    predicate_list_tri = ["the user finds the task too hard", "the user finds the task too easy"]
    
    # Load data
    data = load_data(parameter)

    # Evaluate binary predicates
    for gt in predicate_list_bi:
        print("Ground Truth: ", gt)
        y_true, y_pred, interactions = elaborate_data_binary(data, gt)
        binary_cm(y_true, y_pred, gt, parameter["level"], parameter["sentence"], interactions)
        print("next")

    # Evaluate three-class predicates
    print("Ground Truth List: ", predicate_list_tri)
    y_true, y_pred, interactions = elaborate_data_multiclass(data, predicate_list_tri)
    multiclass_cm(y_true, y_pred, predicate_list_tri, parameter["level"], parameter["sentence"], interactions)
    print("next")