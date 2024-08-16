import pandas as pd
import glob
import pickle
import numpy as np

import collections

features = ['bwd_iat_tot',
            'flow_duration',
            'fwd_iat_tot',
            'idle_min',
            'idle_mean',
            'bwd_iat_max',
            'fwd_iat_max',
            'flow_iat_max',
            'idle_max',
            'flow_pkts_s',
            'label']

def transforma_nomes_colunas(df):
    """
    Transforma os nomes das colunas em letras minúsculas e substitui espaços por underscores.

    Args:
        df (pd.DataFrame): O DataFrame com as colunas a serem transformadas.

    Returns:
        pd.DataFrame: O DataFrame com os nomes das colunas transformados.
    """
    # Obtém os nomes das colunas atuais
    colunas_atuais = df.columns

    # Transforma os nomes das colunas
    novos_nomes = [coluna.lower().replace(" ", "_") for coluna in colunas_atuais]

    # Atribui os novos nomes às colunas do DataFrame
    df.columns = novos_nomes

    return df

def format_df(df):
    df.columns = df.columns.str.replace("/", "_")
    df.columns = df.columns.str.replace("packets", "pkts")
    df.columns = df.columns.str.replace("total", "tot")

    df = df[features]

    df = df.replace([np.inf, -np.inf], np.NaN)
    df = df.replace(np.NaN, 0)

    df = df.drop(columns=["label"])
    return df

def load_csv_folder(folder_path):

    files = glob.glob(f"{folder_path}/*.csv")

    df = []

    for file in files:
        csv_data = pd.read_csv(file)
        df.append(csv_data)
    
    df = pd.concat(df, ignore_index=True)

    df = transforma_nomes_colunas(df)

    df = format_df(df)
    
    return df

df_attack = load_csv_folder("cicflowmeter/attack_output")

df_benign = load_csv_folder("cicflowmeter/benign_output")



modelNamePath = "models/RFC/model-RFC-SYN-2024-04-04_14-19-39.pkl"

model = pickle.load(open(modelNamePath, 'rb'))

df = pd.concat([df_attack, df_benign], ignore_index=True)

predicted = model.predict(df)

from sklearn.metrics import confusion_matrix, recall_score

labels_attack = ['Syn'] * (len(df_attack))
df_labels_attack = pd.DataFrame({'Label': labels_attack})

labels_benign = ['BENIGN'] * (len(df_benign))
df_labels_benign = pd.DataFrame({'Label': labels_benign})

df_actual = pd.concat([df_labels_attack, df_labels_benign], ignore_index=True)

# Compute the confusion matrix
cm = confusion_matrix(df_actual, predicted, labels=['Syn', 'BENIGN'])
tn, fp, fn, tp = confusion_matrix(df_actual, predicted).ravel()
# Print the confusion matrix
print(cm)

print("tn = ", tn)
print("fp = ", fp)
print("fn = ", fn)
print("tp = ", tp)



print(collections.Counter(predicted))
print(predicted)
print("Size:", df.size)


accuracy = (tp + tn) / (tp + fn + fp + tn)
precision = tp / (tp + fp)
recall = recall_score(df_actual, predicted, pos_label="Syn")  # Calculate recall score
f1_score = 2 * (precision * recall) / (precision + recall)

data = {"Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp}

results_df = pd.DataFrame(data, index=[0])

# Save to a file with timestamp
timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"scikit/results_{timestamp}.csv"
results_df.to_csv(filename, index=False)

print(f"Relevant data (including feature names) saved to {filename}")