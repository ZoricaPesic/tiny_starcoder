import os
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import pandas as pd
from scipy.stats import pearsonr


def create_dataset(folder,middles):
    inputs=[]
    for filename in os.listdir(folder):
        with open(os.path.join(folder,filename),'r') as file:

            code=file.read()
            code_length=len(code)
            prefix_ind= random.randint(0,code_length)
            middle_ind= random.randint(prefix_ind,code_length)

            prefix=code[:prefix_ind]
            middle=code[prefix_ind:middle_ind]
            suffix=code[middle_ind:]

            middles.append(middle)

            fim_string=format_fim(prefix,suffix)
            save_to_file(fim_string)
            inputs.append(fim_string)
    return inputs



def format_fim(prefix,suffix):
    return (
        f"<fim_prefix>{prefix}"
        f"<fim_suffix>{suffix}"
        f"<fim_middle>"
            )


def save_to_file(code):
    with open("input.txt", "w") as file:
        file.write(code)


def format_to_code(fim_code):
    prefix=fim_code.split("<fim_suffix>")[0]
    suffix_and_middle=fim_code.split("<fim_suffix>")[1]
    middle=suffix_and_middle.split("<fim_middle>")[1]
    suffix=suffix_and_middle.split("<fim_middle>")[0]
    return (prefix+middle+suffix).replace("<fim_prefix>","").replace("<fim_middle>","").replace("<fim_suffix>","").replace("<|endoftext|>","")


def get_middle(fim_code):
    return fim_code.split("<fim_middle>")[1].replace("<|endoftext|>","")


def evaluate(middles, predictions):
    result=[]
    for i in range(len(middles)):

        exact_match = middles[i] == predictions[i]

        chrf=sentence_chrf(middles[i],predictions[i])

        bleu=sentence_bleu([middles[i].split(" ")],predictions[i].split(" "))


        scorer=rouge_scorer.RougeScorer(['rougeL'], use_stemmer='True')
        rouge=scorer.score(middles[i],predictions[i])['rougeL'].fmeasure

        result.append((exact_match,chrf,bleu,rouge))
    return result


def predict_code():
    predictions=[]

    for input_text in input_texts:
        inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
        outputs = model.generate(inputs, max_length=2000)
        predictions.append(get_middle(tokenizer.decode(outputs[0])))
    return predictions


def print_result(middles,predictions,results):
    for i in range(len(middles)):
        print("MIDDLE")
        print(middles[i],"\n")
        print("PREDICTION")
        print(predictions[i],"\n")
        print("RESULTS")
        print(results[i],"\n")

def calculate_correlation():
    df = pd.read_csv("output.csv")
    df["EM"]=df["EM"].astype(int)
    for metric in ['EM', 'ChrF', 'Bleu', 'RougeL']:
        pearson_corr, _ = pearsonr(df[metric], df['Label'])
        print(metric, " ",pearson_corr)

if __name__ == '__main__':
    middles=[]

    input_texts=create_dataset("code", middles)

    checkpoint = "bigcode/tiny_starcoder_py"
    device = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    predictions=predict_code()

    results=evaluate(middles,predictions)

    calculate_correlation()